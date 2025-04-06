import React, { useState } from 'react';
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
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';

const mockProspects = [
  {
    id: 1,
    prospect_id: 'PROS-12345678',
    name: 'Thomas Anderson',
    email: 'tanderson@example.com',
    phone: '555-123-4567',
    status: 'qualified',
    source: 'Website',
    created_at: '2024-03-10'
  },
  {
    id: 2,
    prospect_id: 'PROS-23456789',
    name: 'Jessica Williams',
    email: 'jwilliams@example.com',
    phone: '555-234-5678',
    status: 'contacted',
    source: 'Social Media',
    created_at: '2024-03-15'
  },
  {
    id: 3,
    prospect_id: 'PROS-34567890',
    name: 'Robert Chen',
    email: 'rchen@example.com',
    phone: '555-345-6789',
    status: 'screening',
    source: 'Referral',
    created_at: '2024-03-20'
  }
];

const mockQualifications = [
  {
    id: 1,
    prospect_id: 'PROS-12345678',
    study_id: 'PROTO-12345678',
    study_name: 'Evaluation of Novel Immunotherapy',
    status: 'qualified',
    notes: 'Meets all inclusion criteria',
    assessed_date: '2024-03-12'
  },
  {
    id: 2,
    prospect_id: 'PROS-12345678',
    study_id: 'PROTO-87654321',
    study_name: 'Cardiovascular Outcomes Study',
    status: 'disqualified',
    notes: 'History of cardiovascular disease',
    assessed_date: '2024-03-12'
  },
  {
    id: 3,
    prospect_id: 'PROS-23456789',
    study_id: 'PROTO-12345678',
    study_name: 'Evaluation of Novel Immunotherapy',
    status: 'pending',
    notes: 'Awaiting medical history',
    assessed_date: '2024-03-16'
  }
];

const mockContactLogs = [
  {
    id: 1,
    prospect_id: 'PROS-12345678',
    contact_type: 'email',
    contact_date: '2024-03-11',
    subject: 'Initial Contact',
    notes: 'Sent introduction email with study information',
    status: 'completed'
  },
  {
    id: 2,
    prospect_id: 'PROS-12345678',
    contact_type: 'phone',
    contact_date: '2024-03-13',
    subject: 'Follow-up Call',
    notes: 'Discussed study details and answered questions',
    status: 'completed'
  },
  {
    id: 3,
    prospect_id: 'PROS-23456789',
    contact_type: 'email',
    contact_date: '2024-03-16',
    subject: 'Initial Contact',
    notes: 'Sent introduction email with study information',
    status: 'completed'
  }
];

const getStatusBadge = (status: string) => {
  const statusMap: Record<string, { label: string, variant: "default" | "secondary" | "destructive" | "outline" }> = {
    qualified: { label: 'Qualified', variant: 'default' },
    disqualified: { label: 'Disqualified', variant: 'destructive' },
    pending: { label: 'Pending', variant: 'outline' },
    contacted: { label: 'Contacted', variant: 'secondary' },
    screening: { label: 'Screening', variant: 'outline' },
    enrolled: { label: 'Enrolled', variant: 'default' },
    completed: { label: 'Completed', variant: 'default' },
    scheduled: { label: 'Scheduled', variant: 'outline' }
  };

  const config = statusMap[status] || { label: status, variant: 'outline' };
  return <Badge variant={config.variant}>{config.label}</Badge>;
};

export function Recruiting() {
  const [selectedProspect, setSelectedProspect] = useState<string | null>(null);

  const filteredQualifications = selectedProspect 
    ? mockQualifications.filter(q => q.prospect_id === selectedProspect)
    : mockQualifications;

  const filteredContactLogs = selectedProspect
    ? mockContactLogs.filter(c => c.prospect_id === selectedProspect)
    : mockContactLogs;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Recruiting Platform</h1>
      
      <Tabs defaultValue="prospects" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="prospects">Prospects</TabsTrigger>
          <TabsTrigger value="qualifications">Study Qualifications</TabsTrigger>
          <TabsTrigger value="contacts">Contact Logs</TabsTrigger>
        </TabsList>
        
        <TabsContent value="prospects" className="space-y-4">
          <div className="flex justify-between mb-4">
            <h2 className="text-xl font-semibold">Prospect Registry</h2>
            <Button>Add New Prospect</Button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {mockProspects.map(prospect => (
              <Card key={prospect.id} className="cursor-pointer hover:shadow-md transition-shadow" 
                onClick={() => setSelectedProspect(prospect.prospect_id)}>
                <CardHeader>
                  <div className="flex items-center space-x-4">
                    <Avatar>
                      <AvatarFallback>{prospect.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                    </Avatar>
                    <div>
                      <CardTitle>{prospect.name}</CardTitle>
                      <CardDescription>{prospect.prospect_id}</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Status:</span>
                      {getStatusBadge(prospect.status)}
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Email:</span>
                      <span className="text-sm">{prospect.email}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Phone:</span>
                      <span className="text-sm">{prospect.phone}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Source:</span>
                      <span className="text-sm">{prospect.source}</span>
                    </div>
                  </div>
                </CardContent>
                <CardFooter>
                  <span className="text-sm text-gray-500">
                    Created: {prospect.created_at}
                  </span>
                </CardFooter>
              </Card>
            ))}
          </div>
        </TabsContent>
        
        <TabsContent value="qualifications">
          <div className="flex justify-between mb-4">
            <h2 className="text-xl font-semibold">
              {selectedProspect 
                ? `Qualifications for ${mockProspects.find(p => p.prospect_id === selectedProspect)?.name}` 
                : 'All Study Qualifications'}
            </h2>
            <div className="space-x-2">
              {selectedProspect && (
                <Button variant="outline" onClick={() => setSelectedProspect(null)}>
                  Clear Filter
                </Button>
              )}
              <Button>Add Qualification</Button>
            </div>
          </div>
          
          <Table>
            <TableCaption>List of study qualifications</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead>Prospect ID</TableHead>
                <TableHead>Study</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Notes</TableHead>
                <TableHead>Assessment Date</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredQualifications.map(qualification => (
                <TableRow key={qualification.id}>
                  <TableCell>{qualification.prospect_id}</TableCell>
                  <TableCell>{qualification.study_name}</TableCell>
                  <TableCell>{getStatusBadge(qualification.status)}</TableCell>
                  <TableCell>{qualification.notes}</TableCell>
                  <TableCell>{qualification.assessed_date}</TableCell>
                  <TableCell>
                    <Button variant="outline" size="sm">Update</Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TabsContent>
        
        <TabsContent value="contacts">
          <div className="flex justify-between mb-4">
            <h2 className="text-xl font-semibold">
              {selectedProspect 
                ? `Contact Logs for ${mockProspects.find(p => p.prospect_id === selectedProspect)?.name}` 
                : 'All Contact Logs'}
            </h2>
            <div className="space-x-2">
              {selectedProspect && (
                <Button variant="outline" onClick={() => setSelectedProspect(null)}>
                  Clear Filter
                </Button>
              )}
              <Button>Log Contact</Button>
            </div>
          </div>
          
          <Table>
            <TableCaption>List of prospect contact logs</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead>Prospect ID</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Subject</TableHead>
                <TableHead>Notes</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredContactLogs.map(contact => (
                <TableRow key={contact.id}>
                  <TableCell>{contact.prospect_id}</TableCell>
                  <TableCell className="capitalize">{contact.contact_type}</TableCell>
                  <TableCell>{contact.contact_date}</TableCell>
                  <TableCell>{contact.subject}</TableCell>
                  <TableCell>{contact.notes}</TableCell>
                  <TableCell>{getStatusBadge(contact.status)}</TableCell>
                  <TableCell>
                    <Button variant="outline" size="sm">View</Button>
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

export default Recruiting;
