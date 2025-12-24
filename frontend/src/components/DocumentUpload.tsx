import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface UploadedFile {
  id: number;
  filename: string;
  status: string;
}

interface DocumentUploadProps {
  sellerId?: number;
  onUploadComplete?: (document: UploadedFile) => void;
}

const ALLOWED_TYPES = [
  "application/pdf",
  "image/jpeg",
  "image/png",
  "image/gif",
  "application/msword",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
];

export function DocumentUpload({ sellerId, onUploadComplete }: DocumentUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const uploadFile = async (file: File) => {
    if (!ALLOWED_TYPES.includes(file.type)) {
      setError(`File type "${file.type}" is not allowed`);
      return;
    }

    setIsUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const url = sellerId
        ? `http://localhost:8000/api/v1/documents/upload?seller_id=${sellerId}`
        : "http://localhost:8000/api/v1/documents/upload";

      const response = await fetch(url, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Upload failed");
      }

      const document = await response.json();
      const uploadedFile: UploadedFile = {
        id: document.id,
        filename: document.filename,
        status: document.status,
      };

      setUploadedFiles((prev) => [...prev, uploadedFile]);
      onUploadComplete?.(uploadedFile);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setIsUploading(false);
    }
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    files.forEach(uploadFile);
  }, [sellerId]);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files) {
      Array.from(files).forEach(uploadFile);
    }
  };

  return (
    <Card className="w-full max-w-md bg-white/10 backdrop-blur-lg border-white/20">
      <CardHeader>
        <CardTitle className="text-xl text-white">Upload Documents</CardTitle>
        <CardDescription className="text-slate-300">
          Drag & drop files or click to browse
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Drop Zone */}
        <motion.div
          className={`
            relative border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
            transition-colors duration-200
            ${isDragging
              ? "border-purple-400 bg-purple-500/20"
              : "border-white/30 hover:border-white/50"
            }
          `}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <input
            type="file"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            onChange={handleFileSelect}
            accept=".pdf,.jpg,.jpeg,.png,.gif,.doc,.docx"
            multiple
          />
          <div className="space-y-2">
            <div className="text-4xl">📄</div>
            <p className="text-slate-200">
              {isDragging ? "Drop files here" : "Click or drag files"}
            </p>
            <p className="text-xs text-slate-400">
              PDF, Images, Word documents
            </p>
          </div>
        </motion.div>

        {/* Upload Progress */}
        <AnimatePresence>
          {isUploading && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="flex items-center justify-center gap-2 text-purple-300"
            >
              <div className="w-4 h-4 border-2 border-purple-400 border-t-transparent rounded-full animate-spin" />
              <span>Uploading...</span>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Error Message */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="p-3 bg-red-500/20 border border-red-500/30 rounded-lg text-red-300 text-sm"
            >
              {error}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Uploaded Files List */}
        <AnimatePresence>
          {uploadedFiles.length > 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="space-y-2"
            >
              <p className="text-sm text-slate-300 font-medium">Uploaded Files</p>
              {uploadedFiles.map((file) => (
                <motion.div
                  key={file.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex items-center justify-between p-2 bg-green-500/20 border border-green-500/30 rounded-lg"
                >
                  <span className="text-sm text-green-300 truncate">
                    {file.filename}
                  </span>
                  <span className="text-xs text-green-400 bg-green-500/20 px-2 py-1 rounded">
                    {file.status}
                  </span>
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </CardContent>
    </Card>
  );
}
