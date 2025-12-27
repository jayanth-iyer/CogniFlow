import { DocumentUpload } from "@/components/DocumentUpload";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export function DocumentsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Documents</h2>
        <p className="text-muted-foreground">Manage and upload seller verification documents.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Upload Document</CardTitle>
              <CardDescription>Drag and drop files here to process them.</CardDescription>
            </CardHeader>
            <CardContent>
              <DocumentUpload />
            </CardContent>
          </Card>
        </div>

        {/* Placeholder for Document List */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Recent Uploads</CardTitle>
              <CardDescription>List of recently processed documents.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-sm text-muted-foreground flex items-center justify-center p-8 border-2 border-dashed rounded-lg">
                No documents found (Placeholder)
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
