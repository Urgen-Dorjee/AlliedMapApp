# 🏥 AlliedMapApp

A **Streamlit-based data transformation application** designed to convert healthcare worker data from Allied format to BlueSky format. This specialized tool eliminates manual data entry and ensures consistent formatting for healthcare staffing system migrations.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 **Overview**

AlliedMapApp streamlines the migration process from Allied healthcare staffing systems to BlueSky platforms by providing:

- **Intelligent Field Mapping**: Auto-mapping with manual override capabilities
- **Data Deduplication**: Eliminates duplicate specialties and certifications
- **Multi-format Processing**: Handles Excel inputs and generates CSV outputs
- **User-friendly Interface**: Clean, intuitive Streamlit web application

## ✨ **Key Features**

### 🗺️ **Smart Field Mapping**
- **Auto-mapping**: Automatically matches fields with identical names
- **Manual Override**: Dropdown selectors for custom field mapping
- **Column Normalization**: Intelligent handling of field name variations

### 📋 **Advanced Data Processing**
- **General Info**: Direct field mapping with required defaults
- **Required Docs**: Extracts and processes certifications into separate rows
- **Specialties**: Deduplicates and compacts specialty information
- **Data Validation**: Handles empty values and data type consistency

### 📤 **Flexible Output Options**
- Individual CSV downloads for each data category
- Bulk ZIP download with all transformed files
- BlueSky-compatible formatting

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.7 or higher
- Required Python packages:
  ```bash
  pip install streamlit pandas openpyxl
  ```

### **Installation**
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Urgen-Dorjee/AlliedMapApp.git
   cd AlliedMapApp
   ```

2. **Run the application:**
   ```bash
   # Windows
   cd Mapper
   Allied.bat
   
   # Linux/Mac
   cd Mapper/system
   streamlit run main.py
   ```

3. **Access the application:**
   - Open your browser to `http://localhost:8501`

## 📖 **How to Use**

### **Step 1: Prepare Your Files**
You'll need:
- **Allied Excel Export**: Your source data file
- **BlueSky Templates**: Three CSV template files:
  - Caregiver General Info Template
  - Caregiver Required Docs Template  
  - Caregiver Specialty Template

### **Step 2: Upload Files**
1. Upload your Allied Excel file
2. Upload all three BlueSky CSV templates
3. The app will automatically load and preview your data

### **Step 3: Map Fields**
1. Review auto-mapped fields in each tab (General Info, Required Docs, Specialty)
2. Use dropdown selectors to manually map any unmapped fields
3. The app preserves your mapping choices during the session

### **Step 4: Process & Download**
1. Click "Process and Generate CSVs"
2. Preview the transformed data in organized tabs
3. Download individual CSV files or the complete ZIP package

## 🔄 **Data Transformation Examples**

### **Specialty Deduplication**
**Input (Allied Format):**
| Id | Allied/Ancillary Specialty 1 | Allied/Ancillary Specialty 2 | Allied/Ancillary Specialty 3 |
|----|------------------------------|------------------------------|------------------------------|
| 123 | Physical Therapy | Physical Therapy | ICU |
| 456 | Nursing, Radiology | Nursing | Emergency |

**Output (BlueSky Format):**
| Person_key | Specialty | Complete | Complete Date | Expiration Date |
|------------|-----------|----------|---------------|-----------------|
| 123 | Physical Therapy | | | |
| 123 | ICU | | | |
| 456 | Nursing | | | |
| 456 | Radiology | | | |
| 456 | Emergency | | | |

### **Certification Processing**
**Input:**
| Id | Allied Certifications |
|----|----------------------|
| 123 | BLS, ACLS, PALS |

**Output:**
| Person_key | CertificationCredentialName | IssueComment | Expiration Date |
|------------|----------------------------|--------------|-----------------|
| 123 | BLS | | |
| 123 | ACLS | | |
| 123 | PALS | | |

## 📁 **Project Structure**

```
AlliedMapApp/
├── Mapper/
│   ├── Allied.bat              # Windows launcher
│   └── system/
│       ├── main.py             # Main Streamlit application
│       ├── mapping.py          # Field mapping logic
│       ├── processing.py       # Data transformation functions
│       ├── setup.py            # Configuration and defaults
│       ├── globals.py          # Global constants
│       ├── helpers.py          # Utility functions
│       ├── ui_helpers.py       # UI components
│       └── license_extraction.py
├── README.md                   # This file
├── LICENSE                     # MIT License
└── .gitignore                  # Git ignore rules
```

## ⚙️ **Configuration**

### **Default Values**
The application includes sensible defaults for required fields:
```python
REQUIRED_DEFAULTS = {
    "Region": "Unknown Region",
    "Fname": "Not Provided", 
    "Lname": "Not Provided",
    "Category": "Not Provided",
    "Status": "Active"
}
```

### **Field Mapping**
Common field mappings are pre-configured:
```python
FALLBACK_MAP = {
    "Person_key": "Id",
    "Fname": "First Name",
    "Lname": "Last Name",
    "ZIPCode": "Postal Code",
    "EMail": "Email"
}
```

## 🛠️ **Technical Details**

### **Core Technologies**
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Python**: Core programming language

### **Key Functions**
- `get_mapping()`: Handles field mapping interface
- `apply_mapping()`: Applies user-defined mappings
- `process_specialties()`: Deduplicates and processes specialties
- `process_required_docs()`: Extracts certification data

### **Data Processing Features**
- **Case-insensitive deduplication**: Handles "ICU" vs "icu"
- **Comma-separated value splitting**: Processes multi-value fields
- **Order preservation**: Maintains first occurrence order
- **Null safety**: Graceful handling of empty/missing data

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 **Support**

If you encounter any issues or have questions:

1. Check the application logs in your terminal
2. Ensure all required files are uploaded correctly
3. Verify your Excel file format matches expected Allied export structure
4. Create an issue in this repository for bugs or feature requests

## 🎉 **Acknowledgments**

- Built for healthcare organizations transitioning from Allied to BlueSky systems
- Designed to eliminate manual data entry and reduce migration errors
- Focused on data integrity and user experience

---

**Made with ❤️ for healthcare data migration**
