from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
import csv
import io

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Only CSV files are supported")
    
    try:
        contents = await file.read()
        
        # Use Python's built-in CSV reader instead of pandas for now
        csv_text = contents.decode('utf-8')
        csv_reader = csv.reader(io.StringIO(csv_text))
        
        # Get header and first few rows
        header = next(csv_reader)
        preview_rows = []
        for i, row in enumerate(csv_reader):
            if i < 5:  # First 5 rows
                preview_rows.append(row)
            else:
                break
        
        session_id = str(uuid.uuid4())
        
        return {
            "session_id": session_id,
            "filename": file.filename,
            "columns": header,
            "preview": preview_rows,
            "row_count": sum(1 for _ in csv.reader(io.StringIO(csv_text))) - 1  # minus header
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error processing file: {str(e)}")
