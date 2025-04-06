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

const mockDonors = [
  {
    id: 1,
    donor_id: 'DNR-12345678',
    name: 'Emily Johnson',
    blood_type: 'O+',
    status: 'active',
    hla_type: 'HLA-A24',
    last_donation: '2024-03-15'
  },
  {
    id: 2,
    donor_id: 'DNR-23456789',
    name: 'David Wilson',
    blood_type: 'A-',
    status: 'inactive',
    hla_type: 'HLA-B27',
    last_donation: '2023-11-20'
  },
  {
    id: 3,
    donor_id: 'DNR-34567890',
    name: 'Sarah Martinez',
    blood_type: 'AB+',
    status: 'pending',
    hla_type: 'HLA-C07',
    last_donation: null
  }
];

const mockDonations = [
  {
    id: 1,
    donation_id: 'DON-12345678',
    donor_id: 'DNR-12345678',
    donor_name: 'Emily Johnson',
    donation_type: 'Whole Blood',
    donation_date: '2024-03-15',
    volume_ml: 450,
    status: 'completed'
  },
  {
    id: 2,
    donation_id: 'DON-23456789',
    donor_id: 'DNR-12345678',
    donor_name: 'Emily Johnson',
    donation_type: 'Plasma',
    donation_date: '2024-01-10',
    volume_ml: 600,
    status: 'completed'
  },
  {
    id: 3,
    donation_id: 'DON-34567890',
    donor_id: 'DNR-23456789',
    donor_name: 'David Wilson',
    donation_type: 'Platelets',
    donation_date: '2023-11-20',
    volume_ml: 250,
    status: 'completed'
  }
];

const mockSamples = [
  {
    id: 1,
    sample_id: 'SAMP-12345678',
    donation_id: 'DON-12345678',
    sample_type: 'Whole Blood',
    volume_ml: 450,
    storage_location: 'Freezer A-12',
    collection_date: '2024-03-15',
    expiration_date: '2024-04-15',
    status: 'available'
  },
  {
    id: 2,
    sample_id: 'SAMP-23456789',
    donation_id: 'DON-12345678',
    sample_type: 'Plasma',
    volume_ml: 200,
    storage_location: 'Freezer B-05',
    collection_date: '2024-03-15',
    expiration_date: '2025-03-15',
    status: 'available'
  },
  {
    id: 3,
    sample_id: 'SAMP-34567890',
    donation_id: 'DON-23456789',
    sample_type: 'Serum',
    volume_ml: 50,
    storage_location: 'Freezer C-18',
    collection_date: '2023-11-20',
    expiration_date: '2024-11-20',
    status: 'reserved'
  }
];

const getStatusBadge = (status: string) => {
  const statusMap: Record<string, { label: string, variant: "default" | "secondary" | "destructive" | "outline" }> = {
    active: { label: 'Active', variant: 'default' },
    inactive: { label: 'Inactive', variant: 'outline' },
    pending: { label: 'Pending', variant: 'secondary' },
    completed: { label: 'Completed', variant: 'default' },
    scheduled: { label: 'Scheduled', variant: 'outline' },
    cancelled: { label: 'Cancelled', variant: 'destructive' },
    available: { label: 'Available', variant: 'default' },
    reserved: { label: 'Reserved', variant: 'secondary' },
    used: { label: 'Used', variant: 'outline' },
    expired: { label: 'Expired', variant: 'destructive' }
  };

  const config = statusMap[status] || { label: status, variant: 'outline' };
  return <Badge variant={config.variant}>{config.label}</Badge>;
};

export function DonationManagement() {
  const [selectedDonor, setSelectedDonor] = useState<string | null>(null);

  const filteredDonations = selectedDonor 
    ? mockDonations.filter(d => d.donor_id === selectedDonor)
    : mockDonations;

  const donorDonationIds = filteredDonations.map(d => d.donation_id);
  const filteredSamples = selectedDonor
    ? mockSamples.filter(s => donorDonationIds.includes(s.donation_id))
    : mockSamples;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Donation Management</h1>
      
      <Tabs defaultValue="donors" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="donors">Donors</TabsTrigger>
          <TabsTrigger value="donations">Donations</TabsTrigger>
          <TabsTrigger value="samples">Samples</TabsTrigger>
        </TabsList>
        
        <TabsContent value="donors" className="space-y-4">
          <div className="flex justify-between mb-4">
            <h2 className="text-xl font-semibold">Donor Registry</h2>
            <Button>Add New Donor</Button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {mockDonors.map(donor => (
              <Card key={donor.id} className="cursor-pointer hover:shadow-md transition-shadow" 
                onClick={() => setSelectedDonor(donor.donor_id)}>
                <CardHeader>
                  <div className="flex items-center space-x-4">
                    <Avatar>
                      <AvatarFallback>{donor.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                    </Avatar>
                    <div>
                      <CardTitle>{donor.name}</CardTitle>
                      <CardDescription>{donor.donor_id}</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Status:</span>
                      {getStatusBadge(donor.status)}
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Blood Type:</span>
                      <span>{donor.blood_type}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">HLA Type:</span>
                      <span>{donor.hla_type}</span>
                    </div>
                  </div>
                </CardContent>
                <CardFooter>
                  <span className="text-sm text-gray-500">
                    Last Donation: {donor.last_donation || 'No donations yet'}
                  </span>
                </CardFooter>
              </Card>
            ))}
          </div>
        </TabsContent>
        
        <TabsContent value="donations">
          <div className="flex justify-between mb-4">
            <h2 className="text-xl font-semibold">
              {selectedDonor 
                ? `Donations for ${mockDonors.find(d => d.donor_id === selectedDonor)?.name}` 
                : 'All Donations'}
            </h2>
            <div className="space-x-2">
              {selectedDonor && (
                <Button variant="outline" onClick={() => setSelectedDonor(null)}>
                  Clear Filter
                </Button>
              )}
              <Button>Schedule Donation</Button>
            </div>
          </div>
          
          <Table>
            <TableCaption>List of donations</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead>Donation ID</TableHead>
                <TableHead>Donor</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Volume (ml)</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredDonations.map(donation => (
                <TableRow key={donation.id}>
                  <TableCell>{donation.donation_id}</TableCell>
                  <TableCell>{donation.donor_name}</TableCell>
                  <TableCell>{donation.donation_type}</TableCell>
                  <TableCell>{donation.donation_date}</TableCell>
                  <TableCell>{donation.volume_ml}</TableCell>
                  <TableCell>{getStatusBadge(donation.status)}</TableCell>
                  <TableCell>
                    <Button variant="outline" size="sm">View</Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TabsContent>
        
        <TabsContent value="samples">
          <div className="flex justify-between mb-4">
            <h2 className="text-xl font-semibold">
              {selectedDonor 
                ? `Samples from ${mockDonors.find(d => d.donor_id === selectedDonor)?.name}` 
                : 'All Samples'}
            </h2>
            <div className="space-x-2">
              {selectedDonor && (
                <Button variant="outline" onClick={() => setSelectedDonor(null)}>
                  Clear Filter
                </Button>
              )}
              <Button>Process Sample</Button>
            </div>
          </div>
          
          <Table>
            <TableCaption>List of biological samples</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead>Sample ID</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Volume (ml)</TableHead>
                <TableHead>Storage Location</TableHead>
                <TableHead>Collection Date</TableHead>
                <TableHead>Expiration Date</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredSamples.map(sample => (
                <TableRow key={sample.id}>
                  <TableCell>{sample.sample_id}</TableCell>
                  <TableCell>{sample.sample_type}</TableCell>
                  <TableCell>{sample.volume_ml}</TableCell>
                  <TableCell>{sample.storage_location}</TableCell>
                  <TableCell>{sample.collection_date}</TableCell>
                  <TableCell>{sample.expiration_date}</TableCell>
                  <TableCell>{getStatusBadge(sample.status)}</TableCell>
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

export default DonationManagement;
