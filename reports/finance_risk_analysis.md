# Finance & Operational Risk Report
*Reference Date: 2026-05-15 | Analysis Period: May–June 2026*

---
## 1. Portfolio Summary

| Metric | Value |
|--------|-------|
| Total Invoiced | ₹63,218,902 |
| Total Paid | ₹39,442,442 |
| Total Outstanding | ₹23,786,960 |
| Collection Rate | 62.4% |
| High Risk Cadets | 13 |
| Medium Risk Cadets | 63 |
| Cadets with Data Errors | 4 (C006, C023, C068, C102) |

---
## 2. Data Integrity Alerts — Manual Review Required

> **WARNING:** The following 4 cadets have outstanding_amount ≠ invoiced_amount − paid_amount.
> These records have been EXCLUDED from automated risk scoring until finance team verification.

| Cadet ID | Name | Invoiced | Paid | Recorded Outstanding | Correct Outstanding | Difference |
|----------|------|---------|------|---------------------|--------------------| -----------|
| C006 | Tanya Nair | ₹661,838 | ₹210,048 | ₹461,290 | ₹451,790 | ₹9,500 |
| C023 | Divya Chaudhary | ₹470,013 | ₹281,781 | ₹181,032 | ₹188,232 | ₹-7,200 |
| C068 | Kabir Iyer | ₹205,400 | ₹74,173 | ₹144,227 | ₹131,227 | ₹13,000 |
| C102 | Rohan Sharma | ₹340,937 | ₹120,593 | ₹215,544 | ₹220,344 | ₹-4,800 |

---
## 3. Payment Risk Table (All Cadets)

| cadet_id | Name | Course | Outstanding (₹) | Payment Completion% | Days Since Payment | Risk Score | Risk Level | Reason |
|----------|------|--------|----------------|--------------------|--------------------|------------|------------|--------|
| C062 | Nidhi Dwivedi | PPL | ₹453,777 | 28.8% | 57 | 78.3 | High | High outstanding ratio 71%; 57d since last payment; Only 29% fees paid |
| C140 | Geeta Raman | PPL | ₹456,368 | 29.5% | 53 | 75.8 | High | High outstanding ratio 70%; 53d since last payment; Only 30% fees paid |
| C025 | Kabir Kapoor | PPL | ₹304,521 | 31.1% | 55 | 75.8 | High | 55d since last payment; Only 31% fees paid |
| C098 | Kunal Kulkarni | PPL | ₹197,608 | 31.0% | 52 | 74.3 | High | 52d since last payment; Only 31% fees paid |
| C055 | Tanya Kapoor | CPL | ₹375,599 | 26.2% | 44 | 73.7 | High | High outstanding ratio 74%; Only 26% fees paid |
| C107 | Nikhil Pillai | CPL | ₹454,756 | 30.9% | 50 | 73.4 | High | 50d since last payment; Only 31% fees paid |
| C084 | Vikram Nair | PPL | ₹194,264 | 37.5% | 59 | 73.3 | High | 59d since last payment; Only 37% fees paid |
| C069 | Nikhil Joshi | CPL | ₹316,437 | 39.3% | 59 | 72.0 | High | 59d since last payment; Only 39% fees paid |
| C024 | Arjun Singh | PPL | ₹114,761 | 25.1% | 38 | 71.4 | High | High outstanding ratio 75%; Only 25% fees paid |
| C077 | Sanya Nair | CPL | ₹430,228 | 33.2% | 49 | 71.2 | High | 49d since last payment; Only 33% fees paid |
| C104 | Anjali Kale | CPL | ₹176,186 | 33.5% | 49 | 71.0 | High | 49d since last payment; Only 34% fees paid |
| C112 | Arjun Pillai | CPL | ₹155,848 | 27.3% | 40 | 70.9 | High | High outstanding ratio 73%; Only 27% fees paid |
| C109 | Priya Sharma | CPL | ₹235,734 | 37.0% | 53 | 70.6 | High | 53d since last payment; Only 37% fees paid |
| C033 | Neha Verma | CPL | ₹325,675 | 29.6% | 41 | 69.8 | Medium | High outstanding ratio 70%; Only 30% fees paid |
| C079 | Arjun Kapoor | PPL | ₹215,823 | 34.7% | 48 | 69.7 | Medium | 48d since last payment; Only 35% fees paid |
| C121 | Vikram Malhotra | CPL | ₹456,388 | 29.1% | 40 | 69.7 | Medium | High outstanding ratio 71%; Only 29% fees paid |
| C060 | Gaurav Mishra | CPL | ₹286,415 | 42.8% | 59 | 69.6 | Medium | 59d since last payment |
| C011 | Sanya Gupta | CPL | ₹118,095 | 31.5% | 43 | 69.4 | Medium | Only 32% fees paid |
| C081 | Aditya Sharma | CPL | ₹305,046 | 44.7% | 60 | 68.7 | Medium | 60d since last payment |
| C074 | Tarun Agrawal | PPL | ₹451,538 | 35.2% | 46 | 68.3 | Medium | 46d since last payment; Only 35% fees paid |
| C116 | Varun Shetty | PPL | ₹190,908 | 29.8% | 36 | 67.2 | Medium | High outstanding ratio 70%; Only 30% fees paid |
| C150 | Arjun Patel | PPL | ₹118,996 | 45.9% | 55 | 65.4 | Medium | 55d since last payment |
| C001 | Sanya Verma | CPL | ₹415,025 | 33.9% | 37 | 64.8 | Medium | Only 34% fees paid |
| C056 | Neha Rao | CPL | ₹431,472 | 35.7% | 37 | 63.5 | Medium | Only 36% fees paid |
| C083 | Swati Jain | CPL | ₹295,379 | 41.7% | 44 | 62.8 | Medium | Within acceptable range |
| C002 | Sanya Gupta | CPL | ₹115,580 | 47.6% | 52 | 62.7 | Medium | 52d since last payment |
| C048 | Pooja Pandey | PPL | ₹258,980 | 47.5% | 51 | 62.3 | Medium | 51d since last payment |
| C030 | Aditya Bose | CPL | ₹325,402 | 48.4% | 51 | 61.7 | Medium | 51d since last payment |
| C004 | Vikram Malhotra | PPL | ₹193,930 | 33.5% | 30 | 61.6 | Medium | Only 33% fees paid |
| C044 | Priya Menon | CPL | ₹161,049 | 45.7% | 46 | 61.0 | Medium | 46d since last payment |
| C120 | Puja Bhat | CPL | ₹179,545 | 54.3% | 58 | 61.0 | Medium | 58d since last payment |
| C139 | Suresh Venkatesan | CPL | ₹370,856 | 33.0% | 28 | 60.9 | Medium | Only 33% fees paid |
| C118 | Sneha Malhotra | CPL | ₹157,516 | 33.8% | 28 | 60.4 | Medium | Only 34% fees paid |
| C078 | Rohan Kapoor | CPL | ₹372,549 | 25.3% | 16 | 60.3 | Medium | High outstanding ratio 75%; Only 25% fees paid |
| C141 | Vinod Gopal | PPL | ₹172,818 | 57.0% | 60 | 60.1 | Medium | 60d since last payment |
| C038 | Aditi Verma | CPL | ₹322,554 | 28.3% | 18 | 59.2 | Medium | High outstanding ratio 72%; Only 28% fees paid |
| C125 | Kabir Singh | PPL | ₹114,213 | 37.8% | 28 | 57.5 | Medium | Only 38% fees paid |
| C053 | Nikhil Gupta | PPL | ₹300,102 | 27.2% | 13 | 57.4 | Medium | High outstanding ratio 73%; Only 27% fees paid |
| C080 | Ananya Nair | CPL | ₹242,216 | 47.6% | 41 | 57.1 | Medium | Within acceptable range |
| C005 | Sneha Sharma | PPL | ₹381,888 | 45.0% | 36 | 56.5 | Medium | Within acceptable range |
| C131 | Seema Kutty | CPL | ₹254,069 | 62.4% | 58 | 55.3 | Medium | 58d since last payment |
| C039 | Nikhil Menon | PPL | ₹175,600 | 63.5% | 58 | 54.6 | Medium | 58d since last payment |
| C019 | Ananya Sharma | CPL | ₹177,491 | 43.0% | 25 | 52.4 | Medium | Within acceptable range |
| C035 | Dev Singh | PPL | ₹172,207 | 49.9% | 34 | 52.1 | Medium | Within acceptable range |
| C021 | Aditya Singh | CPL | ₹61,837 | 59.3% | 46 | 51.5 | Medium | 46d since last payment |
| C012 | Aditi Pillai | CPL | ₹46,589 | 69.7% | 59 | 50.7 | Medium | 59d since last payment |
| C026 | Dev Sharma | CPL | ₹247,564 | 62.0% | 47 | 50.1 | Medium | 47d since last payment |
| C059 | Sunita Tiwari | PPL | ₹223,935 | 49.3% | 28 | 49.5 | Medium | Within acceptable range |
| C092 | Aditya Nair | PPL | ₹152,530 | 68.3% | 52 | 48.2 | Medium | 52d since last payment |
| C119 | Ishaan Iyer | PPL | ₹262,487 | 46.8% | 21 | 47.8 | Medium | Within acceptable range |
| C105 | Arjun Malhotra | CPL | ₹115,553 | 41.8% | 14 | 47.7 | Medium | Within acceptable range |
| C142 | Meera Malhotra | CPL | ₹291,234 | 34.9% | 4 | 47.5 | Medium | Only 35% fees paid |
| C091 | Vivek Desai | PPL | ₹171,037 | 47.4% | 21 | 47.3 | Medium | Within acceptable range |
| C045 | Vikram Sharma | PPL | ₹204,259 | 51.1% | 26 | 47.2 | Medium | Within acceptable range |
| C047 | Tanya Bose | PPL | ₹126,453 | 47.5% | 21 | 47.2 | Medium | Within acceptable range |
| C089 | Shruti Mehta | PPL | ₹78,630 | 55.9% | 31 | 46.4 | Medium | Within acceptable range |
| C063 | Sanya Singh | CPL | ₹204,112 | 52.6% | 26 | 46.1 | Medium | Within acceptable range |
| C022 | Aryan Tripathi | CPL | ₹238,543 | 60.0% | 36 | 46.0 | Medium | Within acceptable range |
| C008 | Priya Kapoor | CPL | ₹422,638 | 38.8% | 4 | 44.9 | Medium | Only 39% fees paid |
| C010 | Dev Kapoor | PPL | ₹282,896 | 51.9% | 22 | 44.7 | Medium | Within acceptable range |
| C028 | Kabir Malhotra | PPL | ₹217,087 | 67.0% | 42 | 44.1 | Medium | Within acceptable range |
| C123 | Rahul Sharma | CPL | ₹116,448 | 67.2% | 42 | 44.0 | Medium | Within acceptable range |
| C058 | Rohan Nair | PPL | ₹211,922 | 45.9% | 12 | 43.9 | Medium | Within acceptable range |
| C106 | Rahul Malhotra | CPL | ₹189,480 | 62.4% | 35 | 43.8 | Medium | Within acceptable range |
| C114 | Vikram Malhotra | CPL | ₹145,362 | 70.4% | 46 | 43.8 | Medium | 46d since last payment |
| C097 | Deepa Patil | PPL | ₹133,412 | 78.8% | 57 | 43.4 | Medium | 57d since last payment |
| C090 | Aditi Gupta | CPL | ₹126,098 | 51.0% | 18 | 43.3 | Medium | Within acceptable range |
| C041 | Rahul Nair | PPL | ₹78,579 | 71.5% | 45 | 42.4 | Medium | Within acceptable range |
| C087 | Manish Shah | PPL | ₹117,328 | 76.2% | 50 | 41.7 | Medium | 50d since last payment |
| C122 | Girish Kamath | CPL | ₹148,395 | 54.8% | 20 | 41.6 | Medium | Within acceptable range |
| C136 | Anita Krishnamurthy | PPL | ₹186,056 | 66.4% | 36 | 41.5 | Medium | Within acceptable range |
| C007 | Rohan Iyer | CPL | ₹73,624 | 51.6% | 15 | 41.4 | Medium | Within acceptable range |
| C113 | Neha Patel | PPL | ₹90,727 | 40.9% | 0 | 41.4 | Medium | Within acceptable range |
| C013 | Dev Gupta | PPL | ₹84,789 | 79.7% | 54 | 41.2 | Medium | 54d since last payment |
| C115 | Smita Hegde | CPL | ₹156,433 | 54.9% | 19 | 41.0 | Medium | Within acceptable range |
| C009 | Rahul Kapoor | CPL | ₹29,179 | 82.6% | 56 | 40.2 | Medium | 56d since last payment |
| C108 | Akash Naik | PPL | ₹109,881 | 70.0% | 37 | 39.5 | Low | Within acceptable range |
| C149 | Rahul Patel | PPL | ₹100,619 | 69.6% | 36 | 39.3 | Low | Within acceptable range |
| C003 | Ishaan Bose | PPL | ₹85,511 | 81.8% | 52 | 38.7 | Low | 52d since last payment |
| C057 | Dev Pillai | CPL | ₹94,913 | 82.7% | 53 | 38.6 | Low | 53d since last payment |
| C017 | Kiran Kapoor | PPL | ₹140,776 | 63.9% | 26 | 38.2 | Low | Within acceptable range |
| C027 | Aditi Kapoor | PPL | ₹184,931 | 61.1% | 22 | 38.2 | Low | Within acceptable range |
| C029 | Tanya Gupta | CPL | ₹39,995 | 82.2% | 50 | 37.5 | Low | 50d since last payment |
| C015 | Ananya Joshi | PPL | ₹78,856 | 84.2% | 52 | 37.1 | Low | 52d since last payment |
| C050 | Neha Sharma | CPL | ₹120,620 | 72.8% | 36 | 37.1 | Low | Within acceptable range |
| C095 | Priya Iyer | PPL | ₹30,119 | 84.6% | 51 | 36.3 | Low | 51d since last payment |
| C086 | Arjun Sharma | CPL | ₹97,796 | 84.6% | 51 | 36.3 | Low | 51d since last payment |
| C014 | Sneha Rao | CPL | ₹83,563 | 81.2% | 46 | 36.2 | Low | 46d since last payment |
| C082 | Sanya Rao | PPL | ₹62,649 | 88.7% | 55 | 35.4 | Low | 55d since last payment |
| C016 | Ishaan Patel | CPL | ₹88,552 | 61.5% | 16 | 34.9 | Low | Within acceptable range |
| C061 | Rohan Singh | PPL | ₹152,152 | 71.0% | 29 | 34.8 | Low | Within acceptable range |
| C110 | Dev Bose | PPL | ₹97,597 | 85.5% | 49 | 34.6 | Low | 49d since last payment |
| C135 | Kiran Bose | CPL | ₹263,678 | 51.9% | 1 | 34.1 | Low | Within acceptable range |
| C049 | Ravi Shukla | PPL | ₹88,336 | 87.0% | 49 | 33.6 | Low | 49d since last payment |
| C070 | Vikram Singh | PPL | ₹48,554 | 68.3% | 22 | 33.2 | Low | Within acceptable range |
| C037 | Harsh Srivastava | CPL | ₹65,199 | 89.8% | 52 | 33.1 | Low | 52d since last payment |
| C034 | Aditya Malhotra | PPL | ₹130,355 | 78.5% | 36 | 33.0 | Low | Within acceptable range |
| C088 | Priya Bose | CPL | ₹157,456 | 70.8% | 25 | 33.0 | Low | Within acceptable range |
| C072 | Rohan Menon | PPL | ₹138,300 | 53.0% | 0 | 32.9 | Low | Within acceptable range |
| C117 | Nikhil Patel | PPL | ₹177,045 | 69.1% | 21 | 32.1 | Low | Within acceptable range |
| C145 | Kiran Rao | PPL | ₹242,640 | 56.7% | 3 | 31.8 | Low | Within acceptable range |
| C051 | Rahul Patel | PPL | ₹96,091 | 65.2% | 14 | 31.4 | Low | Within acceptable range |
| C040 | Sanya Menon | PPL | ₹43,115 | 89.5% | 48 | 31.3 | Low | 48d since last payment |
| C073 | Sneha Gupta | CPL | ₹24,403 | 84.6% | 39 | 30.3 | Low | Within acceptable range |
| C032 | Rohan Malhotra | PPL | ₹137,100 | 66.1% | 13 | 30.2 | Low | Within acceptable range |
| C031 | Ananya Pillai | CPL | ₹191,442 | 71.7% | 20 | 29.8 | Low | Within acceptable range |
| C046 | Ishaan Nair | CPL | ₹216,395 | 68.5% | 15 | 29.5 | Low | Within acceptable range |
| C138 | Tanya Menon | PPL | ₹42,537 | 87.4% | 41 | 29.3 | Low | Within acceptable range |
| C093 | Kiran Malhotra | PPL | ₹159,450 | 71.3% | 17 | 28.6 | Low | Within acceptable range |
| C052 | Nikhil Kapoor | PPL | ₹142,041 | 71.5% | 14 | 26.9 | Low | Within acceptable range |
| C143 | Ananya Verma | CPL | ₹114,309 | 76.0% | 20 | 26.8 | Low | Within acceptable range |
| C043 | Kabir Nair | PPL | ₹91,354 | 71.6% | 12 | 25.9 | Low | Within acceptable range |
| C128 | Kiran Menon | CPL | ₹59,169 | 71.9% | 12 | 25.7 | Low | Within acceptable range |
| C132 | Aditya Pillai | PPL | ₹210,951 | 68.6% | 7 | 25.5 | Low | Within acceptable range |
| C075 | Ishaan Verma | PPL | ₹38,801 | 76.1% | 14 | 23.7 | Low | Within acceptable range |
| C146 | Pushpa Murthy | PPL | ₹35,262 | 93.9% | 38 | 23.3 | Low | Within acceptable range |
| C076 | Kabir Rao | PPL | ₹104,906 | 84.5% | 23 | 22.4 | Low | Within acceptable range |
| C099 | Tanya Verma | CPL | ₹70,419 | 86.8% | 26 | 22.3 | Low | Within acceptable range |
| C147 | Hemant Reddy | PPL | ₹12,735 | 96.3% | 39 | 22.1 | Low | Within acceptable range |
| C127 | Rahul Patel | CPL | ₹28,846 | 89.1% | 28 | 21.6 | Low | Within acceptable range |
| C064 | Neha Nair | PPL | ₹51,942 | 81.2% | 16 | 21.2 | Low | Within acceptable range |
| C137 | Sneha Nair | PPL | ₹105,689 | 80.0% | 14 | 21.0 | Low | Within acceptable range |
| C130 | Meera Bose | CPL | ₹39,250 | 90.5% | 26 | 19.7 | Low | Within acceptable range |
| C100 | Rahul Gupta | CPL | ₹17,706 | 93.5% | 30 | 19.6 | Low | Within acceptable range |
| C133 | Paresh Subramaniam | PPL | ₹9,526 | 96.4% | 34 | 19.5 | Low | Within acceptable range |
| C144 | Aditi Menon | PPL | ₹68,667 | 74.3% | 2 | 19.0 | Low | Within acceptable range |
| C094 | Ananya Menon | CPL | ₹42,641 | 81.0% | 11 | 18.8 | Low | Within acceptable range |
| C020 | Kiran Sharma | CPL | ₹19,550 | 89.8% | 23 | 18.7 | Low | Within acceptable range |
| C148 | Sudha Kumar | CPL | ₹76,070 | 86.4% | 18 | 18.5 | Low | Within acceptable range |
| C096 | Sanya Gupta | PPL | ₹32,235 | 93.8% | 28 | 18.3 | Low | Within acceptable range |
| C018 | Ananya Patel | CPL | ₹56,534 | 75.4% | 1 | 17.8 | Low | Within acceptable range |
| C054 | Nikhil Malhotra | PPL | ₹111,887 | 83.7% | 10 | 16.4 | Low | Within acceptable range |
| C066 | Sneha Singh | CPL | ₹12,438 | 97.9% | 26 | 14.5 | Low | Within acceptable range |
| C036 | Vikram Malhotra | PPL | ₹45,735 | 80.8% | 2 | 14.4 | Low | Within acceptable range |
| C085 | Priya Gupta | CPL | ₹65,535 | 81.2% | 2 | 14.2 | Low | Within acceptable range |
| C126 | Kiran Joshi | PPL | ₹18,972 | 91.3% | 16 | 14.1 | Low | Within acceptable range |
| C101 | Priti Pawar | PPL | ₹24,324 | 95.0% | 20 | 13.5 | Low | Within acceptable range |
| C065 | Rohan Joshi | PPL | ₹18,320 | 95.0% | 18 | 12.5 | Low | Within acceptable range |
| C103 | Sameer Bhosale | CPL | ₹24,271 | 95.3% | 18 | 12.3 | Low | Within acceptable range |
| C129 | Naveen Thampi | PPL | ₹27,657 | 88.8% | 6 | 10.8 | Low | Within acceptable range |
| C111 | Kabir Pillai | PPL | ₹19,625 | 91.4% | 8 | 10.0 | Low | Within acceptable range |
| C067 | Sanya Malhotra | CPL | ₹2,011 | 99.0% | 18 | 9.7 | Low | Within acceptable range |
| C042 | Rohan Gupta | PPL | ₹72 | 100.0% | 19 | 9.5 | Low | Within acceptable range |
| C134 | Meera Iyer | PPL | ₹10,751 | 97.2% | 7 | 5.5 | Low | Within acceptable range |
| C071 | Meera Pillai | CPL | ₹20,904 | 96.4% | 4 | 4.5 | Low | Within acceptable range |
| C124 | Lata Nambiar | CPL | ₹2,508 | 99.5% | 0 | 0.4 | Low | Within acceptable range |
| C006 | Tanya Nair | PPL | ₹461,290 | 31.7% | 15 | N/A | DATA ERROR | Data integrity error — manual review required |
| C023 | Divya Chaudhary | CPL | ₹181,032 | 60.0% | 9 | N/A | DATA ERROR | Data integrity error — manual review required |
| C068 | Kabir Iyer | CPL | ₹144,227 | 36.1% | 16 | N/A | DATA ERROR | Data integrity error — manual review required |
| C102 | Rohan Sharma | PPL | ₹215,544 | 35.4% | 35 | N/A | DATA ERROR | Data integrity error — manual review required |

---
## 4. High Risk Cadets — Immediate Action Required

- **C062 — Nidhi Dwivedi (PPL):** ₹453,777 outstanding | Risk Score: 78.3 | High outstanding ratio 71%; 57d since last payment; Only 29% fees paid
- **C140 — Geeta Raman (PPL):** ₹456,368 outstanding | Risk Score: 75.8 | High outstanding ratio 70%; 53d since last payment; Only 30% fees paid
- **C025 — Kabir Kapoor (PPL):** ₹304,521 outstanding | Risk Score: 75.8 | 55d since last payment; Only 31% fees paid
- **C098 — Kunal Kulkarni (PPL):** ₹197,608 outstanding | Risk Score: 74.3 | 52d since last payment; Only 31% fees paid
- **C055 — Tanya Kapoor (CPL):** ₹375,599 outstanding | Risk Score: 73.7 | High outstanding ratio 74%; Only 26% fees paid
- **C107 — Nikhil Pillai (CPL):** ₹454,756 outstanding | Risk Score: 73.4 | 50d since last payment; Only 31% fees paid
- **C084 — Vikram Nair (PPL):** ₹194,264 outstanding | Risk Score: 73.3 | 59d since last payment; Only 37% fees paid
- **C069 — Nikhil Joshi (CPL):** ₹316,437 outstanding | Risk Score: 72.0 | 59d since last payment; Only 39% fees paid
- **C024 — Arjun Singh (PPL):** ₹114,761 outstanding | Risk Score: 71.4 | High outstanding ratio 75%; Only 25% fees paid
- **C077 — Sanya Nair (CPL):** ₹430,228 outstanding | Risk Score: 71.2 | 49d since last payment; Only 33% fees paid

---
## 5. Recommendations

1. **Immediate collections action** on all High Risk cadets — training continuity at risk if fees remain unpaid.
2. **Finance team manual review** of C006, C023, C068, C102 — correct outstanding amounts in Skynet before next billing cycle.
3. **Skynet billing module** should auto-compute outstanding as invoiced − paid and flag discrepancies at record save time.
4. **Revenue at risk:** ₹3,866,087 across 13 high-risk cadets.
5. **Payment plan option:** Offer structured EMI plan to medium-risk cadets to prevent them escalating to high risk.