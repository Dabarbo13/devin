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

const mockProducts = [
  {
    id: 1,
    product_id: 'PROD-12345678',
    name: 'Whole Blood Sample',
    description: 'Standard whole blood sample from healthy donors',
    price: 199.99,
    category: 'Blood Products',
    inventory: 25,
    attributes: ['Healthy Donor', 'Age 25-45', 'No Medications']
  },
  {
    id: 2,
    product_id: 'PROD-23456789',
    name: 'PBMC Isolation Kit',
    description: 'Peripheral Blood Mononuclear Cells isolation kit',
    price: 349.99,
    category: 'Cell Products',
    inventory: 15,
    attributes: ['Fresh Isolation', 'High Viability', 'Research Grade']
  },
  {
    id: 3,
    product_id: 'PROD-34567890',
    name: 'Serum Panel - Autoimmune',
    description: 'Serum samples from donors with autoimmune conditions',
    price: 499.99,
    category: 'Specialty Panels',
    inventory: 8,
    attributes: ['Verified Diagnosis', 'Complete Medical History', 'Multiple Donors']
  }
];

const mockOrders = [
  {
    id: 1,
    order_id: 'ORD-12345678',
    customer_name: 'University Research Lab',
    order_date: '2024-03-15',
    total_amount: 1049.97,
    status: 'processing',
    items: 3
  },
  {
    id: 2,
    order_id: 'ORD-23456789',
    customer_name: 'BioTech Industries',
    order_date: '2024-03-10',
    total_amount: 2499.95,
    status: 'shipped',
    items: 5
  },
  {
    id: 3,
    order_id: 'ORD-34567890',
    customer_name: 'Medical Research Institute',
    order_date: '2024-03-05',
    total_amount: 899.98,
    status: 'delivered',
    items: 2
  }
];

const mockBuyers = [
  {
    id: 1,
    name: 'University Research Lab',
    contact_person: 'Dr. Emily Johnson',
    email: 'ejohnson@url.example.com',
    phone: '555-123-4567',
    status: 'approved',
    orders_count: 5
  },
  {
    id: 2,
    name: 'BioTech Industries',
    contact_person: 'Dr. Michael Chen',
    email: 'mchen@biotech.example.com',
    phone: '555-234-5678',
    status: 'approved',
    orders_count: 12
  },
  {
    id: 3,
    name: 'Medical Research Institute',
    contact_person: 'Dr. Sarah Williams',
    email: 'swilliams@mri.example.com',
    phone: '555-345-6789',
    status: 'pending',
    orders_count: 3
  }
];

const getStatusBadge = (status: string) => {
  const statusMap: Record<string, { label: string, variant: "default" | "secondary" | "destructive" | "outline" }> = {
    approved: { label: 'Approved', variant: 'default' },
    pending: { label: 'Pending', variant: 'secondary' },
    rejected: { label: 'Rejected', variant: 'destructive' },
    processing: { label: 'Processing', variant: 'secondary' },
    shipped: { label: 'Shipped', variant: 'default' },
    delivered: { label: 'Delivered', variant: 'default' },
    cancelled: { label: 'Cancelled', variant: 'destructive' }
  };

  const config = statusMap[status] || { label: status, variant: 'outline' };
  return <Badge variant={config.variant}>{config.label}</Badge>;
};

export function WebStore() {
  const [cartItems, setCartItems] = useState<number[]>([]);
  
  const addToCart = (productId: number) => {
    setCartItems([...cartItems, productId]);
  };
  
  const cartItemCount = cartItems.length;

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Research Material Web Store</h1>
        <div className="flex items-center space-x-2">
          <Button variant="outline" className="relative">
            Cart
            {cartItemCount > 0 && (
              <span className="absolute -top-2 -right-2 bg-blue-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                {cartItemCount}
              </span>
            )}
          </Button>
          <Button>Checkout</Button>
        </div>
      </div>
      
      <Tabs defaultValue="products" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="products">Products</TabsTrigger>
          <TabsTrigger value="orders">Orders</TabsTrigger>
          <TabsTrigger value="buyers">Institutional Buyers</TabsTrigger>
        </TabsList>
        
        <TabsContent value="products" className="space-y-4">
          <div className="flex justify-between mb-4">
            <h2 className="text-xl font-semibold">Available Products</h2>
            <Button>Add New Product</Button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {mockProducts.map(product => (
              <Card key={product.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <CardTitle>{product.name}</CardTitle>
                  <CardDescription>{product.product_id}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <p className="text-sm">{product.description}</p>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Category:</span>
                      <span className="text-sm">{product.category}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Price:</span>
                      <span className="text-sm font-semibold">${product.price.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">In Stock:</span>
                      <span className="text-sm">{product.inventory} units</span>
                    </div>
                    <div className="mt-2">
                      <span className="text-sm text-gray-500">Attributes:</span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {product.attributes.map((attr, index) => (
                          <Badge key={index} variant="outline">{attr}</Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
                <CardFooter>
                  <Button 
                    className="w-full" 
                    onClick={() => addToCart(product.id)}
                    disabled={product.inventory === 0}
                  >
                    Add to Cart
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        </TabsContent>
        
        <TabsContent value="orders">
          <div className="flex justify-between mb-4">
            <h2 className="text-xl font-semibold">Order History</h2>
            <Button>Create Order</Button>
          </div>
          
          <Table>
            <TableCaption>List of orders</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead>Order ID</TableHead>
                <TableHead>Customer</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Items</TableHead>
                <TableHead>Total</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockOrders.map(order => (
                <TableRow key={order.id}>
                  <TableCell>{order.order_id}</TableCell>
                  <TableCell>{order.customer_name}</TableCell>
                  <TableCell>{order.order_date}</TableCell>
                  <TableCell>{order.items}</TableCell>
                  <TableCell>${order.total_amount.toFixed(2)}</TableCell>
                  <TableCell>{getStatusBadge(order.status)}</TableCell>
                  <TableCell className="space-x-2">
                    <Button variant="outline" size="sm">View</Button>
                    <Button variant="outline" size="sm">Update</Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TabsContent>
        
        <TabsContent value="buyers">
          <div className="flex justify-between mb-4">
            <h2 className="text-xl font-semibold">Institutional Buyers</h2>
            <Button>Add New Buyer</Button>
          </div>
          
          <Table>
            <TableCaption>List of approved institutional buyers</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead>Institution</TableHead>
                <TableHead>Contact Person</TableHead>
                <TableHead>Email</TableHead>
                <TableHead>Phone</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Orders</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockBuyers.map(buyer => (
                <TableRow key={buyer.id}>
                  <TableCell>{buyer.name}</TableCell>
                  <TableCell>{buyer.contact_person}</TableCell>
                  <TableCell>{buyer.email}</TableCell>
                  <TableCell>{buyer.phone}</TableCell>
                  <TableCell>{getStatusBadge(buyer.status)}</TableCell>
                  <TableCell>{buyer.orders_count}</TableCell>
                  <TableCell className="space-x-2">
                    <Button variant="outline" size="sm">View</Button>
                    <Button variant="outline" size="sm">Edit</Button>
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

export default WebStore;
