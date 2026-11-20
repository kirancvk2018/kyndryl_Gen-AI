# Module 3, Lab 1: Multimodal GenAI - Image Analysis for IT Infrastructure

## Overview

This lab teaches learners how to use multimodal Generative AI models to analyze IT infrastructure images. Participants will analyze server racks, monitoring dashboards, network topology diagrams, error screenshots, and system logs using OpenAI's Vision API (or Anthropic Claude) to extract insights, identify issues, and generate incident reports.

## Learning Objectives

By the end of this lab, participants will:

1. ✅ Load and display infrastructure images
2. ✅ Use multimodal AI models to analyze images
3. ✅ Extract structured insights from unstructured image data
4. ✅ Identify anomalies and potential issues
5. ✅ Generate automated incident reports
6. ✅ Build batch image processing workflows
7. ✅ Export analysis results for IT operations teams

## Prerequisites

- Python 3.8+
- OpenAI API key with Vision model access (or Anthropic API key)
- Familiarity with Python, Jupyter notebooks
- Basic understanding of REST APIs

## Project Structure

```
module3_lab1/
├── README.md                              (this file)
├── requirements.txt                       (Python dependencies)
├── module3_lab1_image_analysis.ipynb      (Main Jupyter notebook)
├── generate_sample_images.py              (Sample image generator)
├── .env.example                           (Environment template)
├── sample_images/                         (Generated infrastructure images)
│   ├── 01_server_rack.png
│   ├── 02_monitoring_dashboard.png
│   ├── 03_network_topology.png
│   ├── 04_error_screenshot.png
│   ├── 05_data_center_layout.png
│   └── 06_alert_log.png
├── analysis_results/                      (Analysis outputs)
│   ├── *_insights.json                    (Structured analysis)
│   └── batch_summary_*.json               (Batch processing results)
└── incident_reports/                      (Generated reports)
    └── INC-*.txt                          (Formatted incident tickets)
```

## Setup Instructions

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r module3_requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the lab directory:

```bash
cp .env.example .env
```

Then edit `.env` and add your API key:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional: Anthropic API
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

### 3. Generate Sample Images

Run the image generator to create synthetic infrastructure images:

```bash
python generate_sample_images.py
```

This creates 6 sample images in the `sample_images/` directory:
- **01_server_rack.png** - Server rack with health status
- **02_monitoring_dashboard.png** - 24-hour monitoring metrics
- **03_network_topology.png** - Network architecture diagram
- **04_error_screenshot.png** - Application error window
- **05_data_center_layout.png** - Data center floor plan
- **06_alert_log.png** - System alert log

### 4. Launch Jupyter Notebook

```bash
jupyter notebook module3_lab1_image_analysis.ipynb
```

## Lab Workflow

### Phase 1: Image Loading & Display
```python
# List available images
images = list_images()

# Display a specific image
display_image('sample_images/01_server_rack.png', 
              title='Server Rack Analysis')
```

### Phase 2: Image Analysis
```python
# Analyze a single image
result = analyze_infrastructure_image(
    'sample_images/01_server_rack.png',
    analysis_type='server_rack'
)

# View analysis results
print(result['analysis'])
```

### Phase 3: Structured Insights Extraction
```python
# Extract JSON-structured insights
insights = extract_structured_insights('sample_images/02_monitoring_dashboard.png')

# Access structured data
print(f"Health Status: {insights['health_status']}")
print(f"Issues: {insights['issues']}")
print(f"Recommendations: {insights['recommendations']}")
```

### Phase 4: Incident Report Generation
```python
# Generate formal incident report
report = generate_incident_report(image_path, analysis_result)

# Save report to file
save_incident_report(report, ticket_id='INC-20240115-001')
```

### Phase 5: Batch Processing
```python
# Analyze all images in directory
results = batch_analyze_images(
    image_directory='sample_images',
    analysis_type='general'
)

# View summary
for result in results:
    print(f"{result['image']}: {result['status']}")
```

## Image Types & Analysis Modes

The notebook supports different analysis types optimized for specific infrastructure scenarios:

### 1. **General Analysis**
- Overview of infrastructure components
- Initial health assessment
- Broad issue identification

### 2. **Server Rack Analysis**
- Equipment inventory
- Cable management assessment
- Power distribution status
- Cooling/ventilation observations
- Specific rack optimization recommendations

### 3. **Dashboard Analysis**
- Metric extraction and interpretation
- Trend identification
- Alert status assessment
- Performance anomaly detection

### 4. **Network Analysis**
- Network topology interpretation
- Connectivity assessment
- Redundancy evaluation
- Security considerations

### 5. **Error Analysis**
- Error message extraction
- Root cause identification
- Severity assessment
- Remediation steps

## Output Files

### Incident Reports (`.txt`)
Located in `incident_reports/`

```
================================================================================
                     IT INFRASTRUCTURE INCIDENT REPORT
================================================================================

TICKET ID:           INC-20240115143522
REPORT DATE:         2024-01-15 14:35:22
SOURCE IMAGE:        01_server_rack.png
ANALYSIS MODEL:      claude-3-5-sonnet

[Analysis content...]
```

### Structured Insights (`.json`)
Located in `analysis_results/`

```json
{
  "image_type": "server_rack",
  "health_status": "warning",
  "components": ["WEB-01", "WEB-02", "DB-01", ...],
  "issues": ["High CPU on STORAGE-01", "Memory pressure on DB-02"],
  "severity": "high",
  "recommendations": [...]
}
```

### Batch Summary (`.json`)
Contains processing results for all images in batch job

```json
[
  {"image": "sample_images/01_server_rack.png", "status": "success"},
  {"image": "sample_images/02_monitoring_dashboard.png", "status": "success"},
  ...
]
```

## Key Functions Reference

### Image Management
- `list_images(directory)` - List all images in directory
- `display_image(path, title)` - Display image with title
- `encode_image_to_base64(path)` - Encode for API submission

### Analysis
- `analyze_infrastructure_image(path, analysis_type)` - Analyze with vision model
- `extract_structured_insights(path)` - Extract JSON-structured data
- `complete_image_analysis_workflow(path, analysis_type)` - Full analysis pipeline

### Reporting
- `generate_incident_report(path, analysis_result)` - Create incident ticket
- `save_incident_report(report, ticket_id)` - Save to file
- `batch_analyze_images(directory, analysis_type)` - Process multiple images

### Export
- `export_analysis_to_csv(directory)` - Export results to CSV
- `print_summary_stats()` - Display analysis statistics

## API Costs & Optimization

### Cost Considerations
- Vision model calls: ~$0.01 per image (OpenAI)
- Batch processing: Scale costs with image count
- Storage: Minimal (images + JSON results)

### Cost Optimization Tips
1. **Resize large images** before processing
2. **Batch similar images** together
3. **Cache results** to avoid re-processing
4. **Use structured prompts** for faster responses

## Troubleshooting

### Common Issues

**"OPENAI_API_KEY not found"**
```bash
# Check .env file exists and is properly set
cat .env

# Set environment variable directly (Linux/Mac)
export OPENAI_API_KEY=sk-...

# Or Windows
set OPENAI_API_KEY=sk-...
```

**"Unable to acquire JPEG Connection"**
- This is sample error in screenshots - not a real error in the lab

**"Module not found" errors**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall requirements
pip install -r module3_requirements.txt
```

**Images not generating**
```bash
# Ensure matplotlib backend is available
python -c "import matplotlib; matplotlib.use('TkAgg')"

# Check write permissions to sample_images/
ls -la sample_images/
```

## Exercises for Learners

### Exercise 1: Single Image Analysis
Analyze one infrastructure image and generate a detailed incident report with:
- Component inventory
- Health assessment
- Issue identification
- Recommended actions

### Exercise 2: Comparative Analysis
Compare two dashboard images over time:
- Identify metric trends
- Detect anomalies
- Assess performance changes

### Exercise 3: Batch Processing
Analyze all 6 sample images and:
- Categorize by issue severity
- Generate summary report
- Create alert prioritization list

### Exercise 4: Custom Prompts
Modify analysis prompts for domain-specific scenarios:
- Security audit focus
- Compliance check
- Cost optimization analysis

### Exercise 5: Integration Scenario
Build a monitoring pipeline that:
1. Captures dashboard screenshots hourly
2. Analyzes each with specific focus
3. Escalates critical issues
4. Generates daily summary report

## Real-World Applications

This lab demonstrates practical use cases for IT operations teams:

1. **Incident Response**
   - Automated ticket generation from screenshots
   - Rapid issue categorization
   - Recommended actions

2. **Infrastructure Monitoring**
   - Visual anomaly detection
   - Capacity planning insights
   - Proactive issue identification

3. **Knowledge Management**
   - Searchable incident history
   - Pattern recognition
   - Root cause documentation

4. **Compliance & Auditing**
   - Infrastructure state verification
   - Change tracking
   - Audit trail generation

5. **Training & Onboarding**
   - Visual system documentation
   - Automated architecture diagrams
   - Issue scenario walkthroughs

## Extended Learning

### Topics to Explore
- **RAG Integration**: Combine image analysis with vector databases
- **Multi-step Workflows**: Chain multiple analysis steps
- **Custom Training**: Fine-tune models for domain-specific patterns
- **Real-time Monitoring**: Integrate with live monitoring systems
- **Mobile Integration**: Capture and analyze on-the-go

### Next Steps
- **Module 4**: Build interactive Streamlit/Gradio web application
- **Module 7**: Implement RAG with infrastructure documentation
- **Module 8**: Create autonomous agents for incident management
- **Module 9**: Set up MLflow evaluation and tracking

## Resources

- **OpenAI Vision API**: https://platform.openai.com/docs/guides/vision
- **Anthropic Claude Vision**: https://docs.anthropic.com/claude/reference/vision
- **Matplotlib Documentation**: https://matplotlib.org/
- **Pillow Documentation**: https://pillow.readthedocs.io/

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review notebook comments for clarification
3. Consult API documentation links
4. Ask instructor for guidance

## License

This lab material is provided for educational purposes.

---

**Last Updated**: January 2024
**Version**: 1.0
**Author**: Generative AI Training Program
