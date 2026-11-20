# Module 3, Lab 1 - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Setup (2 min)
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r module3_requirements.txt

# 3. Configure API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Step 2: Generate Sample Images (1 min)
```bash
python generate_sample_images.py
```

You'll see:
```
✓ Generated: 01_server_rack.png
✓ Generated: 02_monitoring_dashboard.png
✓ Generated: 03_network_topology.png
✓ Generated: 04_error_screenshot.png
✓ Generated: 05_data_center_layout.png
✓ Generated: 06_alert_log.png
```

### Step 3: Launch Notebook (1 min)
```bash
jupyter notebook module3_lab1_image_analysis.ipynb
```

### Step 4: Run Cells (1 min)
1. Execute cells sequentially from top to bottom
2. Start with "Setup and Imports" section
3. List images to verify they loaded
4. Run example analysis cells

---

## 📊 What Each Section Does

| Section | Purpose | Time |
|---------|---------|------|
| Setup & Imports | Initialize environment & load API | 30s |
| Load Images | Display infrastructure images | 1m |
| Image Encoding | Prepare images for API | 30s |
| Analyze Images | Send to Vision API, get insights | 2-3m |
| Extract Structure | Parse JSON-structured results | 1m |
| Generate Reports | Create incident tickets | 1m |
| Batch Analysis | Process multiple images | 5-10m |
| Export Results | Save to CSV/JSON | 30s |

---

## 💡 Key Commands

### Analyze Single Image
```python
result = complete_image_analysis_workflow(
    'sample_images/01_server_rack.png',
    analysis_type='server_rack'
)
```

### Analyze All Images
```python
results = batch_analyze_images(
    image_directory='sample_images',
    analysis_type='general'
)
```

### View Results
```python
# List all generated reports
import os
print(os.listdir('incident_reports'))

# Print summary statistics
print_summary_stats()
```

---

## 📁 Output Locations

After running the lab, you'll have:

```
incident_reports/
├── INC-20240115143522.txt      ← Incident ticket
└── INC-20240115143530.txt      ← Another ticket

analysis_results/
├── 01_server_rack_insights.json       ← Structured data
├── 02_monitoring_dashboard_insights.json
└── batch_summary_20240115_143530.json ← Batch results
```

---

## 🎯 Expected Results

### For Each Image:
✅ Detailed analysis text  
✅ Structured JSON insights  
✅ Incident report with ticket ID  
✅ Recommendations for action  

### Example Output:
```
TICKET ID:           INC-20240115143522
REPORT DATE:         2024-01-15 14:35:22
SOURCE IMAGE:        01_server_rack.png

AUTOMATED ANALYSIS SUMMARY
==========================
Server Rack DC-RACK-042 contains 10 server units with...

ISSUES IDENTIFIED
- STORAGE-01: Critical CPU usage (95%)
- DB-02: Memory nearing capacity (95%)

RECOMMENDATIONS
1. Immediately investigate STORAGE-01 CPU spike
2. Plan memory upgrade for DB-02
3. Check cable management for cooling issues
```

---

## ⚠️ Troubleshooting

### "API Key not found"
```bash
# Verify .env file
cat .env | grep OPENAI_API_KEY

# Re-export if needed
export OPENAI_API_KEY=sk-...
```

### "Module not found"
```bash
# Make sure venv is activated
which python  # Should show venv path

# Reinstall
pip install -r module3_requirements.txt
```

### "No images generated"
```bash
# Run the generator again
python generate_sample_images.py

# Check directory
ls -la sample_images/
```

### "API rate limited"
- Wait a minute before retrying
- Reduce batch size
- Use smaller images

---

## 🎓 Learning Path

### Beginner
1. ✅ Run single image analysis
2. ✅ View generated incident reports
3. ✅ Review structured insights

### Intermediate
1. ✅ Modify analysis prompts
2. ✅ Change analysis types
3. ✅ Run batch processing
4. ✅ Export results to CSV

### Advanced
1. ✅ Integrate with monitoring systems
2. ✅ Chain multiple analyses
3. ✅ Build custom evaluation metrics
4. ✅ Deploy as microservice

---

## 📚 Next Steps

After completing this lab:

1. **Module 3, Lab 2**: Build interactive Streamlit web app
2. **Module 4**: Advanced multimodal workflows
3. **Module 5**: Prompt engineering for specific domains
4. **Module 7**: Combine with RAG and vector databases

---

## 💬 Tips for Instructors

### Demo Setup (3 min)
```bash
# Pre-generate images
python generate_sample_images.py

# Have notebook ready
jupyter notebook module3_lab1_image_analysis.ipynb
```

### Live Demo Flow
1. Show notebook structure (1 min)
2. Run "Load Images" section (30s)
3. Run analysis on 1 image (2 min)
4. Show generated report (30s)
5. Run batch processing (3 min)
6. Show results (1 min)

### Common Q&A
- **"Can we use real infrastructure images?"** → Yes! Replace sample images
- **"How do we integrate with live systems?"** → See Module 4
- **"Can we customize the report format?"** → Yes! Modify template
- **"What about cost?"** → ~$0.01 per image with OpenAI

---

## 📞 Support

- Check **MODULE3_LAB1_README.md** for detailed docs
- Review notebook comments for inline help
- Check API provider docs for rate limits
- Ask instructor for custom scenarios

---

**Version 1.0** | **Last Updated: Jan 2024**
