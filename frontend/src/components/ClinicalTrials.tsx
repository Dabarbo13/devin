import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow, TableCaption } from './ui/table';
import { Badge } from './ui/badge';
import { useQuery, useLazyQuery } from '@apollo/client'; // Updated imports
import { GET_STUDIES_LIST, GET_PARTICIPANTS_FOR_STUDY } from '../graphql/queries'; // Updated imports
import { Sheet, SheetContent, SheetTrigger } from './ui/sheet';
import AddStudyForm from './AddStudyForm';

// Mock data for visits - to be replaced later
const mockVisits = [
  { id: 'v1', participantId: 'p1', date: '2023-02-01', type: 'Baseline', status: 'Completed' },
  { id: 'v2', participantId: 'p1', date: '2023-03-01', type: 'Follow-up 1', status: 'Scheduled' },
  { id: 'v3', participantId: 'p2', date: '2023-02-15', type: 'Screening Visit', status: 'Completed' },
];

// Helper function for status badge styling (can be reused for participant status if needed)
const getStatusBadge = (status: string) => {
  switch (status?.toLowerCase()) {
    case 'recruiting':
      return <Badge variant="default" className="bg-green-500 text-white">Recruiting</Badge>;
    case 'active':
    case 'enrolled': // Participant status
      return <Badge variant="default" className="bg-blue-500 text-white">{status}</Badge>;
    case 'completed':
      return <Badge variant="secondary">Completed</Badge>;
    case 'on_hold': 
    case 'on hold':
      return <Badge variant="outline" className="bg-yellow-500 text-white">On Hold</Badge>;
    case 'terminated':
      return <Badge variant="destructive">Terminated</Badge>;
    case 'screening': // Participant status
      return <Badge variant="default" className="bg-purple-500 text-white">Screening</Badge>;
    default:
      return <Badge variant="outline">{status || 'Unknown'}</Badge>;
  }
};


export function ClinicalTrials() {
  const { loading: studiesLoading, error: studiesError, data: studiesData } = useQuery(GET_STUDIES_LIST);
  const [
    loadParticipants, 
    { loading: participantsLoading, error: participantsError, data: participantsData }
  ] = useLazyQuery(GET_PARTICIPANTS_FOR_STUDY);
  
  const [isAddStudySheetOpen, setIsAddStudySheetOpen] = useState(false);
  const [visits, setVisits] = useState(mockVisits); // Keep for now
  const [selectedStudy, setSelectedStudy] = useState<string | null>(null);

  const studies = studiesData?.studies || [];
  const currentParticipants = participantsData?.participants || [];

  // Filter visits based on currently displayed participants (if any)
  const selectedStudyParticipantIds = new Set(currentParticipants.map((p: any) => p.id));
  const filteredVisits = selectedStudy ? visits.filter(v => selectedStudyParticipantIds.has(v.participantId)) : [];

  const handleStudySelect = (studyId: string) => {
    setSelectedStudy(studyId);
    loadParticipants({ variables: { studyId: studyId } });
  };

  const handleStudyAdded = (newStudyData: any) => {
    console.log('New study added, data to potentially update cache or list:', newStudyData);
    setIsAddStudySheetOpen(false); 
    // GET_STUDIES_LIST query is refetched by AddStudyForm's useMutation hook
  };

  if (studiesLoading) return <p className="text-center p-4">Loading studies...</p>;
  if (studiesError) return <p className="text-center p-4 text-red-600">Error fetching studies: {studiesError.message}</p>;

  return (
    <div className="container mx-auto p-4">
      <header className="mb-6">
        <h1 className="text-3xl font-bold">Clinical Trials Management</h1>
        <p className="text-gray-600">Overview and management of ongoing and upcoming clinical trials.</p>
      </header>

      <Tabs defaultValue="studies" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="studies">Studies</TabsTrigger>
          <TabsTrigger value="participants" disabled={!selectedStudy && !participantsLoading}>Participants</TabsTrigger>
          <TabsTrigger value="visits" disabled={!selectedStudy && !participantsLoading}>Visits</TabsTrigger>
        </TabsList>

        {/* Studies Tab Content */}
        <TabsContent value="studies" className="space-y-4">
          <div className="flex justify-between items-center mt-4 mb-4">
            <h2 className="text-xl font-semibold">Clinical Studies</h2>
            <Sheet open={isAddStudySheetOpen} onOpenChange={setIsAddStudySheetOpen}>
              <SheetTrigger asChild>
                <Button onClick={() => setIsAddStudySheetOpen(true)}>Add New Study</Button>
              </SheetTrigger>
              <SheetContent className="md:w-2/3 lg:w-1/2 xl:w-1/3 sm:w-full p-0 overflow-y-auto">
                <AddStudyForm 
                  onClose={() => setIsAddStudySheetOpen(false)} 
                  onStudyAdded={handleStudyAdded} 
                />
              </SheetContent>
            </Sheet>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {studies.map((study: any) => (
              <Card 
                key={study.id} 
                className={`cursor-pointer hover:shadow-lg transition-shadow ${selectedStudy === study.id ? 'ring-2 ring-blue-500 shadow-lg' : 'shadow-md'}`}
                onClick={() => handleStudySelect(study.id)}
              >
                <CardHeader>
                  <CardTitle>{study.title}</CardTitle>
                  <CardDescription>{study.protocolNumber}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Status:</span>
                      {getStatusBadge(study.status)}
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Phase:</span>
                      <span>{study.phase ? study.phase.replace(/_/g, ' ') : 'N/A'}</span>
                    </div>
                     <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Area:</span>
                      <span>{study.therapeuticArea || 'N/A'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">PI:</span>
                      <span>
                        {study.principalInvestigator 
                         ? `${study.principalInvestigator.firstName || ''} ${study.principalInvestigator.lastName || ''}`.trim() || study.principalInvestigator.email 
                         : 'N/A'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Sponsor:</span>
                      <span>{study.sponsorName || 'N/A'}</span>
                    </div>
                  </div>
                </CardContent>
                <CardFooter className="flex justify-between text-sm text-gray-500">
                  <span>Started: {study.startDate ? new Date(study.startDate).toLocaleDateString() : 'N/A'}</span>
                  <span>Target: {study.targetEnrollment}</span>
                </CardFooter>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Participants Tab Content */}
        <TabsContent value="participants">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">
              {selectedStudy && studies.find((s:any) => s.id === selectedStudy)
                ? `Participants for ${studies.find((s:any) => s.id === selectedStudy)?.protocolNumber}`
                : 'Select a study to view participants'}
            </h2>
            <div className="space-x-2">
              {selectedStudy && (
                <Button variant="outline" onClick={() => {
                  setSelectedStudy(null);
                  // No need to manually clear participantsData for useLazyQuery, it's tied to the query execution
                }}>
                  Clear Selection
                </Button>
              )}
              <Button disabled={!selectedStudy}>Add Participant</Button> 
            </div>
          </div>
          
          {selectedStudy ? (
            participantsLoading ? (
              <p className="text-center p-4">Loading participants...</p>
            ) : participantsError ? (
              <p className="text-center p-4 text-red-600">Error fetching participants: {participantsError.message}</p>
            ) : currentParticipants.length > 0 ? (
              <Table>
                <TableCaption>
                  {`List of participants for study ${studies.find((s:any) => s.id === selectedStudy)?.protocolNumber}`}
                </TableCaption>
                <TableHeader>
                  <TableRow>
                    <TableHead>Participant ID</TableHead>
                    <TableHead>First Name</TableHead>
                    <TableHead>Last Name</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Enrollment Date</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {currentParticipants.map((participant: any) => (
                    <TableRow key={participant.id}>
                      <TableCell>{participant.participantId}</TableCell>
                      <TableCell>{participant.firstName}</TableCell>
                      <TableCell>{participant.lastName}</TableCell>
                      <TableCell>{getStatusBadge(participant.status)}</TableCell>
                      <TableCell>{participant.enrollmentDate ? new Date(participant.enrollmentDate).toLocaleDateString() : 'N/A'}</TableCell>
                      <TableCell>
                        <Button variant="outline" size="sm">View</Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            ) : (
              <p className="text-center p-4">No participants found for this study.</p>
            )
          ) : (
            <p className="text-center p-4">Please select a study to see its participants.</p>
          )}
        </TabsContent>

        {/* Visits Tab Content (remains using mock data for now) */}
        <TabsContent value="visits" className="space-y-4">
          {selectedStudy && (
            <>
              <h2 className="text-xl font-semibold">
                Visits for Study: {studies.find((s: any) => s.id === selectedStudy)?.title || 'Selected Study'}
              </h2>
              <div className="flex justify-end">
                <Button>Schedule New Visit</Button>
              </div>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Visit ID</TableHead>
                    <TableHead>Participant ID</TableHead>
                    <TableHead>Date</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredVisits.length > 0 ? (
                    filteredVisits.map(visit => (
                      <TableRow key={visit.id}>
                        <TableCell>{visit.id}</TableCell>
                        <TableCell>{visit.participantId}</TableCell>
                        <TableCell>{visit.date}</TableCell>
                        <TableCell>{visit.type}</TableCell>
                        <TableCell><Badge variant={visit.status === 'Completed' ? 'default' : 'secondary'}>{visit.status}</Badge></TableCell>
                      </TableRow>
                    ))
                  ) : (
                    <TableRow>
                      <TableCell colSpan={5} className="text-center">No visits scheduled for participants in this study yet.</TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}

export default ClinicalTrials;
