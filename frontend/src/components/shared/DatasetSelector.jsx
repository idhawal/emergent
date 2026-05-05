import { useRef, useState } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Upload, Loader2 } from "lucide-react";
import { uploadDataset } from "@/lib/api";

export default function DatasetSelector({ availableDatasets = [], value, onChange, accept = ".csv" }) {
  const fileRef = useRef(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);

  async function handleFileChange(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    setUploadError(null);
    try {
      const result = await uploadDataset(file);
      onChange("__uploaded__", result);
    } catch (err) {
      setUploadError(err.message);
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  }

  return (
    <div className="space-y-2">
      <Select value={value} onValueChange={(v) => onChange(v)}>
        <SelectTrigger data-testid="dataset-selector" className="bg-neutral-900 border-neutral-700 text-neutral-100">
          <SelectValue placeholder="Select dataset" />
        </SelectTrigger>
        <SelectContent className="bg-neutral-900 border-neutral-700">
          {availableDatasets.map((name) => (
            <SelectItem key={name} value={name} className="text-neutral-100">
              {name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      <input
        ref={fileRef}
        type="file"
        accept={accept}
        className="hidden"
        onChange={handleFileChange}
      />
      <Button
        variant="outline"
        size="sm"
        className="w-full border-neutral-700 bg-neutral-900 text-neutral-300 hover:bg-neutral-800"
        onClick={() => fileRef.current?.click()}
        disabled={uploading}
        data-testid="upload-dataset-btn"
      >
        {uploading ? (
          <Loader2 className="h-3.5 w-3.5 mr-2 animate-spin" />
        ) : (
          <Upload className="h-3.5 w-3.5 mr-2" />
        )}
        {uploading ? "Uploading..." : "Upload CSV"}
      </Button>

      {uploadError && (
        <p className="text-xs text-rose-400 font-mono">{uploadError}</p>
      )}

      {value === "__uploaded__" && (
        <p className="text-xs text-emerald-400 font-mono">Custom dataset loaded</p>
      )}
    </div>
  );
}
