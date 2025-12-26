from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
import spacy
import uvicorn
from pydantic import BaseModel
from docx import Document
from pypdf import PdfReader

app = FastAPI()

# 1. CORS Ayarları (Frontend ile iletişim için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Modelleri Yükle (İngilizce - Garantili Çalışan)
print("⏳ Loading English Models...")
try:
    # Daha önce indirdiğin en_core_web_lg modelini kullanıyoruz
    nlp = spacy.load("en_core_web_lg")
    # Presidio varsayılan olarak İngilizce çalışır, ekstra ayara gerek yok
    analyzer = AnalyzerEngine() 
    anonymizer = AnonymizerEngine()
    print("✅ English Models Ready!")
except Exception as e:
    print(f"❌ Model Error: {e}")
    # Hata olursa yedek olarak küçük modeli dene
    try:
        nlp = spacy.load("en_core_web_sm")
        analyzer = AnalyzerEngine()
        anonymizer = AnonymizerEngine()
        print("⚠️ Switched to small model.")
    except:
        print("❌ Critical: No spacy model found. Please run 'python -m spacy download en_core_web_lg'")

# 3. Yardımcı Fonksiyonlar
def process_anonymization(text: str):
    if not text: return ""
    
    # İngilizce Analiz
    results = analyzer.analyze(
        text=text,
        language='en', 
        entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "LOCATION", "DATE_TIME", "NRP"]
    )

    # Anonimleştirme (Etiketler İngilizce)
    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators={
            "PERSON": OperatorConfig("replace", {"new_value": " [PERSON] "}),
            "PHONE_NUMBER": OperatorConfig("replace", {"new_value": " [PHONE] "}),
            "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": " [EMAIL] "}),
            "LOCATION": OperatorConfig("replace", {"new_value": " [LOCATION] "}),
            "DATE_TIME": OperatorConfig("replace", {"new_value": " [DATE] "}),
            "NRP": OperatorConfig("replace", {"new_value": " [ID_NUMBER] "}), # Nationality/Religious/Political
        }
    )
    return anonymized_result.text

def read_file_content(file: UploadFile) -> str:
    content = ""
    filename = file.filename.lower()
    
    if filename.endswith(".txt"):
        content = file.file.read().decode("utf-8")
        
    elif filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                content += text + "\n"
                
    elif filename.endswith(".docx"):
        doc = Document(file.file)
        for para in doc.paragraphs:
            content += para.text + "\n"
            
    return content

# 4. API Uç Noktaları (Endpoints)
class TextRequest(BaseModel):
    text: str

@app.post("/anonymize")
async def anonymize_text(request: TextRequest):
    # Basit metin isteği
    result = process_anonymization(request.text)
    return {"original": request.text, "result": result}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Dosya yükleme isteği
    try:
        content = read_file_content(file)
        if not content.strip():
            return {"error": "File is empty or could not be read."}
            
        result = process_anonymization(content)
        return {"filename": file.filename, "original": content, "result": result}
    except Exception as e:
        return {"error": str(e)}

# Yerel başlatma
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)