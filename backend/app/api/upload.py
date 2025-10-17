from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import uuid
import json

router = APIRouter()

@router.post(\"/upload\")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, \"Only CSV files are supported\")
    
    try:
        contents = await file.read()
        df = pd.read_csv(pd.compat.StringIO(contents.decode('utf-8')))
        
        session_id = str(uuid.uuid4())
        
        return {
            \"session_id\": session_id,
            \"filename\": file.filename,
            \"columns\": df.columns.tolist(),
            \"shape\": df.shape,
            \"preview\": df.head().to_dict()
        }
        
    except Exception as e:
        raise HTTPException(500, f\"Error processing file: {str(e)}\")
