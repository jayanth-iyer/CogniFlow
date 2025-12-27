import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { useEffect, useState } from "react";
import { Loader2 } from "lucide-react";

interface Seller {
  id: number;
  name: string;
  email: string;
  business_name: string;
  status: string;
  created_at: string;
}

export function SellersPage() {
  const [sellers, setSellers] = useState<Seller[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSellers = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/sellers');
        if (response.ok) {
          const data = await response.json();
          setSellers(data);
        }
      } catch (error) {
        console.error("Failed to fetch sellers", error);
      } finally {
        setLoading(false);
      }
    };
    fetchSellers();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'approved': return 'bg-green-500/10 text-green-500 hover:bg-green-500/20';
      case 'rejected': return 'bg-red-500/10 text-red-500 hover:bg-red-500/20';
      default: return 'bg-yellow-500/10 text-yellow-500 hover:bg-yellow-500/20';
    }
  };

  if (loading) return <div className="flex justify-center p-8"><Loader2 className="animate-spin" /></div>;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Sellers</h2>
        <p className="text-muted-foreground">Manage seller accounts and statuses.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Seller Directory</CardTitle>
          <CardDescription>View and manage registered sellers.</CardDescription>
        </CardHeader>
        <CardContent>
          {sellers.length === 0 ? (
            <div className="text-center p-8 text-muted-foreground">No sellers found.</div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Business Name</TableHead>
                  <TableHead>Contact Name</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {sellers.map((seller) => (
                  <TableRow key={seller.id}>
                    <TableCell className="font-medium">{seller.business_name}</TableCell>
                    <TableCell>{seller.name}</TableCell>
                    <TableCell>{seller.email}</TableCell>
                    <TableCell>
                      <Badge className={getStatusColor(seller.status)} variant="outline">
                        {seller.status}
                      </Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
