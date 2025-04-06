import React, { useState, useEffect } from 'react';
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardFooter, 
  CardHeader, 
  CardTitle 
} from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Badge } from './ui/badge';
import { Button } from './ui/button';

const mockStudies = [
  {
    id: 1,
    title: 'Evaluation of Novel Immunotherapy',
    protocol_number: 'PROTO-12345678',
    status: 'active',
    phase: 'PHASE_2',
    therapeutic_area: 'Oncology',
    principal_investigator: 'Dr. Jane Smith',
    start_date: '2024-01-15',
    target_participants: 120
  },
  {
    id: 2,
    title: 'Cardiovascular Outcomes Study',
    protocol_number: 'PROTO-87654321',
    status: 'pending_approval',
    phase: 'PHASE_3',
    therapeutic_area: 'Cardiology',
    principal_investigator: 'Dr. John Doe',
    start_date: '2024-03-01',
    target_participants: 250
  },
  {
    id: 3,
    title: 'Novel Treatment for Alzheimer\'s Disease',
    protocol_number: 'PROTO-23456789',
    status: 'completed',
    phase: 'PHASE_2',
    therapeutic_area: 'Neurology',
    principal_investigator: 'Dr. Sarah Johnson',
    start_date: '2023-06-10',
    target_participants: 180
  }
];

const mockParticipants = [
  {
    id: 1,
    participant_id: 'PART-12345678',
    name: 'Michael Brown',
    status: 'active',
    site: 'Boston Medical Center',
    enrollment_date: '2024-02-15',
    study_id: 1
  },
  {
    id: 2,
    participant_id: 'PART-23456789',
    name: 'Jennifer Wilson',
    status: 'screening',
    site: 'Boston Medical Center',
    enrollment_date: null,
    study_id: 1
  },
  {
    id: 3,
    participant_id: 'PART-34567890',
    name: 'Robert Davis',
    status: 'completed',
    site: 'Chicago Research Hospital',
    enrollment_date: '2024-01-20',
    study_id: 3
  }
];

const mockVisits = [
  {
    id: 1,
    participant_id: 'PART-12345678',
    visit_name: 'Screening Visit',
    scheduled_date: '2024-02-10',
    status: 'completed',
    site: 'Boston Medical Center'
  },
  {
    id: 2,
    participant_id: 'PART-12345678',
    visit_name: 'Baseline Visit',
    scheduled_date: '2024-02-17',
    status: 'completed',
    site: 'Boston Medical Center'
  },
  {
    id: 3,
    participant_id: 'PART-12345678',
    visit_name: 'Treatment Visit 1',
    scheduled_date: '2024-03-17',
    status: 'scheduled',
    site: 'Boston Medical Center'
  }
];

const getStatusBadge = (status: string) => {
  const statusMap: Record<string, { label: string, variant: "default" | "secondary" | "destructive" | "outline" }> = {
    active: { label: 'Active', variant: 'default' },
    completed: { label: 'Completed', variant: 'secondary' },
    pending_approval: { label: 'Pending Approval', variant: 'outline' },
    draft: { label: 'Draft', variant: 'outline' },
    paused: { label: 'Paused', variant: 'destructive' },
    terminated: { label: 'Terminated', variant: 'destructive' },
    screening: { label: 'Screening', variant: 'outline' },
    enrolled: { label: 'Enrolled', variant: 'default' },
    withdrawn: { label: 'Withdrawn', variant: 'destructive' },
    scheduled: { label: 'Scheduled', variant: 'outline' },
    missed: { label: 'Missed', variant: 'destructive' },
    rescheduled: { label: 'Rescheduled', variant: 'outline' },
    cancelled: { label: 'Cancelled', variant: 'destructive' }
  };

  const config = statusMap[status] || { label: status, variant: 'outline' };
  return <Badge variant={config.variant}>{config.label}</Badge>;
};

export function ClinicalTrials() {
  const [studies, setStudies] = useState(mockStudies);
  const [participants, setParticipants] = useState(mockParticipants);
  const [visits, setVisits] = useState(mockVisits);
  const [selectedStudy, setSelectedStudy] = useState<number | null>(null);

  const filteredParticipants = selectedStudy 
    ? participants.filter(p => p.study_id === selectedStudy)
    : participants;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Clinical Trial Management</h1>
      
      <Tabs defaultValue="studies" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="studies">Studies</TabsTrigger>
          <TabsTrigger value="participants">Participants</TabsTrigger>
          <TabsTrigger value="visits">Visits</TabsTrigger>
        </TabsList>
        
        <TabsContent value="studies" className="space-y-4">
          <div className="flex justify-between mb-4">
            <h2 className="text-xl font-semibold">Clinical Studies</h2>
            <Button>Add New Study</Button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {studies.map(study => (
              <Card key={study.id} className="cursor-pointer hover:shadow-md transition-shadow" 
                onClick={() => setSelectedStudy(study.id)}>
                <CardHeader>
                  <CardTitle>{study.title}</CardTitle>
                  <CardDescription>{study.protocol_number}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Status:</span>
                      {getStatusBadge(study.status)}
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Phase:</span>
                      <span>{study.phase.replace('PHASE_', 'Phase ')}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Area:</span>
                      <span>{study.therapeutic_area}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">PI:</span>
                      <span>{study.principal_investigator}</span>
                    </div>
                  </div>
                </CardContent>
                <CardFooter className="flex justify-between">
                  <span className="text-sm text-gray-500">Started: {study.start_date}</span>
                  <span className="text-sm text-gray-500">Target: {study.target_participants}</span>
                </CardFooter>
              </Card>
            ))}
          </div>
        </TabsContent>
        
        <TabsContent value="participants">
          <div className="flex justify-between mb-4">
            <h2 className="text-xl font-semibold">
              {selectedStudy 
                ? `Participants for ${studies.find(s => s.id === selectedStudy)?.protocol_number}` 
                : 'All Participants'}
            </h2>
            <div className="space-x-2">
              {selectedStudy && (
                <Button variant="outline" onClick={() => setSelectedStudy(null)}>
                  Clear Filter
                </Button>
              )}
              <Button>Add Participant</Button>
            </div>
          </div>
          
          <Table>
            <TableCaption>List of clinical trial participants</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Site</TableHead>
                <TableHead>Enrollment Date</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredParticipants.map(participant => (
                <TableRow key={participant.id}>
                  <TableCell>{participant.participant_id}</TableCell>
                  <TableCell>{participant.name}</TableCell>
                  <TableCell>{getStatusBadge(participant.status)}</TableCell>
                  <TableCell>{participant.site}</TableCell>
                  <TableCell>{participant.enrollment_date || 'Not enrolled'}</TableCell>
                  <TableCell>
                    <Button variant="outline" size="sm">View</Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TabsContent>
        
        <TabsContent value="visits">
          <div className="flex justify-between mb-4">
            <h2 className="text-xl font-semibold">Scheduled Visits</h2>
            <Button>Schedule Visit</Button>
          </div>
          
          <Table>
            <TableCaption>List of scheduled and completed visits</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead>Participant ID</TableHead>
                <TableHead>Visit</TableHead>
                <TableHead>Scheduled Date</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Site</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {visits.map(visit => (
                <TableRow key={visit.id}>
                  <TableCell>{visit.participant_id}</TableCell>
                  <TableCell>{visit.visit_name}</TableCell>
                  <TableCell>{visit.scheduled_date}</TableCell>
                  <TableCell>{getStatusBadge(visit.status)}</TableCell>
                  <TableCell>{visit.site}</TableCell>
                  <TableCell className="space-x-2">
                    <Button variant="outline" size="sm">Edit</Button>
                    <Button variant="outline" size="sm">Complete</Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TabsContent>
      </Tabs>
    </div>
  );
}

export default ClinicalTrials;
