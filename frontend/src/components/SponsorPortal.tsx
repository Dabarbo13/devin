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
import { Avatar, AvatarFallback } from './ui/avatar';

const mockSponsors = [
  {
    id: 1,
    name: 'Novagen Pharmaceuticals',
    contact_person: 'Dr. Elizabeth Chen',
    email: 'echen@novagen.example.com',
    phone: '555-123-4567',
    status: 'active',
    studies_count: 3
  },
  {
    id: 2,
    name: 'BioMedica Research',
    contact_person: 'Dr. James Wilson',
    email: 'jwilson@biomedica.example.com',
    phone: '555-234-5678',
    status: 'active',
    studies_count: 2
  },
  {
    id: 3,
    name: 'GeneTech Solutions',
    contact_person: 'Dr. Sarah Johnson',
    email: 'sjohnson@genetech.example.com',
    phone: '555-345-6789',
    status: 'inactive',
    studies_count: 1
  }
];

const mockResearchers = [
  {
    id: 1,
    name: 'Dr. Michael Brown',
    institution: 'University Medical Center',
    email: 'mbrown@umc.example.com',
    phone: '555-456-7890',
    status: 'active',
    research_area: 'Oncology'
  },
  {
    id: 2,
    name: 'Dr. Jennifer Davis',
    institution: 'National Research Institute',
    email: 'jdavis@nri.example.com',
    phone: '555-567-8901',
    status: 'active',
    research_area: 'Immunology'
  },
  {
    id: 3,
    name: 'Dr. Robert Wilson',
    institution: 'Central Medical School',
    email: 'rwilson@cms.example.com',
    phone: '555-678-9012',
    status: 'pending',
    research_area: 'Neurology'
  }
];

const mockSampleRequests = [
  {
    id: 1,
    request_id: 'REQ-12345678',
    researcher_name: 'Dr. Michael Brown',
    sample_type: 'Whole Blood',
    quantity: 10,
    specifications: 'Healthy donors, age 25-45',
    status: 'pending',
    requested_date: '2024-03-15'
  },
  {
    id: 2,
    request_id: 'REQ-23456789',
    researcher_name: 'Dr. Jennifer Davis',
    sample_type: 'PBMCs',
    quantity: 5,
    specifications: 'Donors with autoimmune conditions',
    status: 'approved',
    requested_date: '2024-03-10'
  },
  {
    id: 3,
    request_id: 'REQ-34567890',
    researcher_name: 'Dr. Robert Wilson',
    sample_type: 'Serum',
    quantity: 15,
    specifications: 'Donors over 65 years old',
    status: 'fulfilled',
    requested_date: '2024-02-20'
  }
];

const getStatusBadge = (status: string) => {
  const statusMap: Record<string, { label: string, variant: "default" | "secondary" | "destructive" | "outline" }> = {
    active: { label: 'Active', variant: 'default' },
    inactive: { label: 'Inactive', variant: 'outline' },
    pending: { label: 'Pending', variant: 'secondary' },
    approved: { label: 'Approved', variant: 'default' },
    rejected: { label: 'Rejected', variant: 'destructive' },
    fulfilled: { label: 'Fulfilled', variant: 'secondary' },
    cancelled: { label: 'Cancelled', variant: 'destructive' }
  };

  const config = statusMap[status] || { label: status, variant: 'outline' };
  return <Badge variant={config.variant}>{config.label}</Badge>;
};

export function SponsorPortal() {
  const [selectedResearcher, setSelectedResearcher] = useState<number | null>(null);

  const filteredRequests = selectedResearcher 
    ? mockSampleRequests.filter(r => r.researcher_name === mockResearchers.find(res => res.id === selectedResearcher)?.name)
    : mockSampleRequests;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Sponsor & Researcher Portal</h1>
      
      <Tabs defaultValue="sponsors" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="sponsors">Sponsors</TabsTrigger>
          <TabsTrigger value="researchers">Researchers</TabsTrigger>
          <TabsTrigger value="requests">Sample Requests</TabsTrigger>
        </TabsList>
        
        <TabsContent value="sponsors" className="space-y-4">
          <div className="flex justify-between mb-4">
            <h2 className="text-xl font-semibold">Sponsor Organizations</h2>
            <Button>Add New Sponsor</Button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {mockSponsors.map(sponsor => (
              <Card key={sponsor.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <CardTitle>{sponsor.name}</CardTitle>
                  <CardDescription>Contact: {sponsor.contact_person}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Status:</span>
                      {getStatusBadge(sponsor.status)}
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Email:</span>
                      <span className="text-sm">{sponsor.email}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Phone:</span>
                      <span className="text-sm">{sponsor.phone}</span>
                    </div>
                  </div>
                </CardContent>
                <CardFooter>
                  <span className="text-sm text-gray-500">
                    Active Studies: {sponsor.studies_count}
                  </span>
                </CardFooter>
              </Card>
            ))}
          </div>
        </TabsContent>
        
        <TabsContent value="researchers">
          <div className="flex justify-between mb-4">
            <h2 className="text-xl font-semibold">Researcher Profiles</h2>
            <Button>Add New Researcher</Button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {mockResearchers.map(researcher => (
              <Card 
                key={researcher.id} 
                className="cursor-pointer hover:shadow-md transition-shadow"
                onClick={() => setSelectedResearcher(researcher.id)}
              >
                <CardHeader>
                  <div className="flex items-center space-x-4">
                    <Avatar>
                      <AvatarFallback>{researcher.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                    </Avatar>
                    <div>
                      <CardTitle>{researcher.name}</CardTitle>
                      <CardDescription>{researcher.institution}</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Status:</span>
                      {getStatusBadge(researcher.status)}
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Research Area:</span>
                      <span className="text-sm">{researcher.research_area}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Email:</span>
                      <span className="text-sm">{researcher.email}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Phone:</span>
                      <span className="text-sm">{researcher.phone}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
        
        <TabsContent value="requests">
          <div className="flex justify-between mb-4">
            <h2 className="text-xl font-semibold">
              {selectedResearcher 
                ? `Sample Requests from ${mockResearchers.find(r => r.id === selectedResearcher)?.name}` 
                : 'All Sample Requests'}
            </h2>
            <div className="space-x-2">
              {selectedResearcher && (
                <Button variant="outline" onClick={() => setSelectedResearcher(null)}>
                  Clear Filter
                </Button>
              )}
              <Button>New Request</Button>
            </div>
          </div>
          
          <Table>
            <TableCaption>List of custom sample requests</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead>Request ID</TableHead>
                <TableHead>Researcher</TableHead>
                <TableHead>Sample Type</TableHead>
                <TableHead>Quantity</TableHead>
                <TableHead>Specifications</TableHead>
                <TableHead>Requested Date</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredRequests.map(request => (
                <TableRow key={request.id}>
                  <TableCell>{request.request_id}</TableCell>
                  <TableCell>{request.researcher_name}</TableCell>
                  <TableCell>{request.sample_type}</TableCell>
                  <TableCell>{request.quantity}</TableCell>
                  <TableCell>{request.specifications}</TableCell>
                  <TableCell>{request.requested_date}</TableCell>
                  <TableCell>{getStatusBadge(request.status)}</TableCell>
                  <TableCell className="space-x-2">
                    <Button variant="outline" size="sm">View</Button>
                    <Button variant="outline" size="sm">Update</Button>
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

export default SponsorPortal;
