import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Any, Dict, List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

@app.get("/api/overview")
def overview() -> Dict[str, Any]:
    """Return simple counts for key collections used by the school system"""
    try:
        from database import db
        if db is None:
            raise HTTPException(status_code=500, detail="Database not configured")
        counts = {}
        for name in ["student", "teacher", "course", "enrollment", "announcement"]:
            try:
                counts[name] = db[name].count_documents({})
            except Exception:
                counts[name] = 0
        return {"ok": True, "counts": counts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/announcements")
def get_announcements(limit: int = 5) -> Dict[str, Any]:
    """Return latest announcements, pinned first then by publish date desc"""
    try:
        from database import db
        if db is None:
            raise HTTPException(status_code=500, detail="Database not configured")
        
        cursor = db["announcement"].find({})
        # Sort: pinned desc, publish_at desc
        try:
            cursor = cursor.sort([("pinned", -1), ("publish_at", -1)])
        except Exception:
            pass
        if limit:
            cursor = cursor.limit(limit)
        items: List[Dict[str, Any]] = []
        for doc in cursor:
            doc["_id"] = str(doc.get("_id"))
            # Normalize optional fields
            if "publish_at" in doc and isinstance(doc["publish_at"], datetime):
                doc["publish_at"] = doc["publish_at"].isoformat()
            items.append(doc)
        return {"ok": True, "items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
