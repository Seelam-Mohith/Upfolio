"""Reference corpus of job descriptions used for TF-IDF keyword discovery.

A pasted JD is compared against these "other JDs" so that terms unique to the
current role stand out (high TF-IDF) even when they aren't in SKILLS_DB.
"""

JD_CORPUS: list[dict[str, str]] = [
    {
        'id': 'frontend',
        'title': 'Frontend Developer',
        'description': "Job Summary\n\nWe are looking for a passionate Frontend Developer to build responsive and interactive web applications using modern JavaScript frameworks. The ideal candidate should have strong UI development skills and a good understanding of performance optimization.\n\nResponsibilities\nBuild responsive web applications using React.\nConvert UI/UX designs into reusable components.\nIntegrate REST APIs.\nOptimize application performance.\nWrite clean, maintainable code.\nCollaborate with backend developers.\nParticipate in code reviews.\n\nRequired Skills\nHTML5\nCSS3\nJavaScript (ES6+)\nTypeScript\nReact.js\nNext.js\nRedux\nTailwind CSS\nREST APIs\nGit\nResponsive Design\n\nPreferred Skills\nVite\nFramer Motion\nJest\nCypress\nFirebase\n\nExperience\n\n0â€“3 Years\n\nEducation\n\nBachelor's Degree in Computer Science or related field.\n\nATS Keywords\n\nReact, JavaScript, TypeScript, HTML, CSS, Tailwind, Frontend, REST API, Git",
    },
    {
        'id': 'backend',
        'title': 'Backend Developer',
        'description': "Job Summary\n\nWe are seeking a Backend Developer to design, develop, and maintain scalable server-side applications and RESTful APIs.\n\nResponsibilities\nDevelop REST APIs.\nDesign scalable backend architecture.\nWork with SQL and NoSQL databases.\nImplement authentication and authorization.\nDeploy backend services.\nOptimize application performance.\n\nRequired Skills\nPython\nFlask\nDjango\nNode.js\nExpress.js\nMySQL\nPostgreSQL\nMongoDB\nREST APIs\nJWT\nDocker\nGit\nLinux\n\nPreferred Skills\nRedis\nGraphQL\nAWS\nCI/CD\n\nExperience\n\n1â€“3 Years\n\nEducation\n\nBachelor's Degree in Computer Science.\n\nATS Keywords\n\nPython, Flask, Django, Backend, REST API, SQL, MongoDB, Docker",
    },
    {
        'id': 'fullstack',
        'title': 'Full Stack Developer',
        'description': "Job Summary\n\nWe are hiring a Full Stack Developer capable of building complete web applications from frontend to backend.\n\nResponsibilities\nDevelop frontend and backend modules.\nBuild APIs.\nDesign databases.\nDeploy applications.\nOptimize performance.\nCollaborate with cross-functional teams.\n\nRequired Skills\nReact\nNode.js\nExpress\nMongoDB\nMySQL\nJavaScript\nTypeScript\nREST APIs\nDocker\nGit\n\nPreferred Skills\nAWS\nFirebase\nCI/CD\n\nExperience\n\n1â€“4 Years\n\nEducation\n\nBachelor's Degree in Computer Science.\n\nATS Keywords\n\nFull Stack, MERN, React, Node.js, MongoDB, Express, JavaScript",
    },
    {
        'id': 'ml-engineer',
        'title': 'Machine Learning Engineer',
        'description': "Job Summary\n\nWe are looking for a Machine Learning Engineer to develop predictive models and deploy machine learning solutions into production.\n\nResponsibilities\nBuild ML models.\nFeature engineering.\nTrain and evaluate algorithms.\nDeploy models.\nMonitor model performance.\n\nRequired Skills\nPython\nNumPy\nPandas\nScikit-learn\nTensorFlow\nPyTorch\nXGBoost\nSQL\nGit\n\nPreferred Skills\nMLflow\nDocker\nAWS\nAzure\n\nExperience\n\n1â€“3 Years\n\nEducation\n\nBachelor's or Master's in Computer Science, AI, or Data Science.\n\nATS Keywords\n\nMachine Learning, Python, TensorFlow, PyTorch, Scikit-learn, XGBoost",
    },
    {
        'id': 'data-scientist',
        'title': 'Data Scientist',
        'description': "Job Summary\n\nWe are seeking a Data Scientist to analyze large datasets, build predictive models, and provide business insights.\n\nResponsibilities\nAnalyze datasets.\nBuild ML models.\nPerform statistical analysis.\nCreate dashboards.\nPresent insights.\n\nRequired Skills\nPython\nSQL\nPandas\nNumPy\nStatistics\nMachine Learning\nTableau\nPower BI\n\nPreferred Skills\nDeep Learning\nAWS\nSpark\n\nExperience\n\n1â€“4 Years\n\nEducation\n\nBachelor's or Master's Degree.\n\n    ATS Keywords\n\nData Science, Statistics, SQL, Python, Tableau, Power BI",
    },
    {
        'id': 'data-analyst',
        'title': 'Data Analyst',
        'description': "Job Summary\n\nWe are looking for a Data Analyst who can transform raw data into meaningful business insights.\n\nResponsibilities\nAnalyze business data.\nCreate reports.\nBuild dashboards.\nPerform SQL queries.\nPresent findings.\n\nRequired Skills\nSQL\nExcel\nPower BI\nTableau\nPython\nPandas\n\nPreferred Skills\nStatistics\nMachine Learning\n\nExperience\n\n0â€“2 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nSQL, Excel, Power BI, Tableau, Python, Data Analysis",
    },
    {
        'id': 'nlp-engineer',
        'title': 'NLP Engineer',
        'description': "Job Summary\n\nWe are looking for an NLP Engineer to build language models and intelligent text processing applications.\n\nResponsibilities\nDevelop NLP pipelines.\nBuild text classification models.\nWork with LLMs.\nDeploy NLP solutions.\n\nRequired Skills\nPython\nspaCy\nNLTK\nHugging Face Transformers\nLangChain\nOpenAI API\nGemini API\nRAG\nVector Databases\n\nPreferred Skills\nFAISS\nPinecone\nChromaDB\n\nExperience\n\n1â€“3 Years\n\nEducation\n\nBachelor's or Master's Degree.\n\nATS Keywords\n\nNLP, LangChain, Transformers, RAG, Hugging Face, spaCy",
    },
    {
        'id': 'genai-engineer',
        'title': 'Generative AI Engineer',
        'description': "Job Summary\n\nWe are hiring a Generative AI Engineer to build AI-powered applications using Large Language Models and Retrieval-Augmented Generation (RAG).\n\nResponsibilities\nBuild GenAI applications.\nDevelop RAG pipelines.\nDesign AI agents.\nIntegrate LLM APIs.\nOptimize prompts.\n\nRequired Skills\nPython\nLangChain\nLangGraph\nOpenAI\nGemini\nClaude\nChromaDB\nPinecone\nFAISS\nPrompt Engineering\nVector Databases\nRAG\n\nPreferred Skills\nMCP\nDocker\nFastAPI\n\nExperience\n\n1â€“3 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nGenAI, LLM, LangChain, RAG, Prompt Engineering, Vector Database",
    },
    {
        'id': 'cv-engineer',
        'title': 'Computer Vision Engineer',
        'description': "Job Summary\n\nWe are seeking a Computer Vision Engineer to develop image and video processing solutions using deep learning.\n\nResponsibilities\nDevelop object detection systems.\nBuild image classification models.\nProcess video streams.\nOptimize inference performance.\n\nRequired Skills\nPython\nOpenCV\nYOLO\nTensorFlow\nPyTorch\nCNN\nImage Processing\n\nPreferred Skills\nOCR\nSegmentation\nONNX\n\nExperience\n\n1â€“3 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nComputer Vision, OpenCV, YOLO, CNN, TensorFlow, PyTorch",
    },
    {
        'id': 'devops',
        'title': 'DevOps Engineer',
        'description': "Job Summary\n\nWe are looking for a DevOps Engineer to automate deployment pipelines, manage cloud infrastructure, and improve software delivery.\n\nResponsibilities\nBuild CI/CD pipelines.\nManage cloud infrastructure.\nContainerize applications.\nMonitor system health.\nAutomate deployments.\n\nRequired Skills\nDocker\nKubernetes\nJenkins\nGitHub Actions\nTerraform\nLinux\nAWS\nAzure\nBash\nGit\n\nPreferred Skills\nPrometheus\nGrafana\nAnsible\n\nExperience\n\n2â€“5 Years\n\nEducation\n\nBachelor's Degree.\n\n    ATS Keywords\n\nDevOps, Docker, Kubernetes, AWS, Terraform, Jenkins, CI/CD",
    },
    {
        'id': 'cloud-engineer',
        'title': 'Cloud Engineer',
        'description': "Job Summary\n\nWe are looking for a Cloud Engineer to design, deploy, and maintain secure, scalable cloud infrastructure. The ideal candidate should have experience with cloud platforms, infrastructure automation, and cloud-native services.\n\nResponsibilities\nDesign and deploy cloud infrastructure.\nConfigure networking and security.\nManage virtual machines and cloud storage.\nAutomate cloud deployments.\nMonitor cloud resources.\nOptimize cloud costs.\n\nRequired Skills\nAWS\nMicrosoft Azure\nGoogle Cloud Platform (GCP)\nEC2\nS3\nLambda\nIAM\nVPC\nDocker\nKubernetes\nTerraform\nLinux\nGit\n\nPreferred Skills\nCloudFormation\nAnsible\nJenkins\n\nExperience\n\n1â€“4 Years\n\nEducation\n\nBachelor's Degree in Computer Science or related field.\n\nATS Keywords\n\nAWS, Azure, GCP, Cloud, Terraform, Kubernetes, Docker",
    },
    {
        'id': 'cybersecurity-analyst',
        'title': 'Cybersecurity Analyst',
        'description': "Job Summary\n\nWe are looking for a Cybersecurity Analyst to monitor, detect, and respond to security threats while ensuring organizational security compliance.\n\nResponsibilities\nMonitor security alerts.\nConduct vulnerability assessments.\nPerform penetration testing.\nInvestigate security incidents.\nMaintain security documentation.\nRecommend security improvements.\n\nRequired Skills\nNetwork Security\nKali Linux\nWireshark\nBurp Suite\nNmap\nMetasploit\nSIEM\nOWASP Top 10\nPython\nLinux\n\nPreferred Skills\nSplunk\nNessus\nCEH Certification\n\nExperience\n\n1â€“3 Years\n\nEducation\n\nBachelor's Degree in Computer Science, Cybersecurity, or related field.\n\nATS Keywords\n\nCybersecurity, Penetration Testing, Kali Linux, Burp Suite, SIEM, OWASP",
    },
    {
        'id': 'qa-automation',
        'title': 'QA Automation Engineer',
        'description': "Job Summary\n\nWe are seeking a QA Automation Engineer to develop automated test scripts and ensure software quality through comprehensive testing.\n\nResponsibilities\nDesign test plans.\nDevelop automated test scripts.\nPerform API testing.\nExecute regression testing.\nReport and track defects.\n\nRequired Skills\nSelenium\nPlaywright\nCypress\nJava\nPython\nTestNG\nJUnit\nPostman\nREST API Testing\nGit\n\nPreferred Skills\nJMeter\nJenkins\n\nExperience\n\n1â€“3 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nAutomation Testing, Selenium, Cypress, Playwright, Postman, API Testing",
    },
    {
        'id': 'mobile-dev',
        'title': 'Mobile Application Developer',
        'description': "Job Summary\n\nWe are hiring a Mobile Application Developer to build cross-platform and native mobile applications with high performance and excellent user experience.\n\nResponsibilities\nDevelop Android and iOS applications.\nIntegrate REST APIs.\nOptimize mobile performance.\nPublish applications.\nFix bugs and improve usability.\n\nRequired Skills\nFlutter\nDart\nReact Native\nKotlin\nSwift\nFirebase\nREST APIs\nSQLite\nGit\n\nPreferred Skills\nFirebase Cloud Messaging\nGoogle Maps API\n\nExperience\n\n0â€“3 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nFlutter, React Native, Android, iOS, Dart, Kotlin, Swift",
    },
    {
        'id': 'blockchain',
        'title': 'Blockchain Developer',
        'description': "Job Summary\n\nWe are seeking a Blockchain Developer to develop decentralized applications and secure smart contracts for blockchain platforms.\n\nResponsibilities\nDevelop smart contracts.\nBuild decentralized applications (DApps).\nIntegrate blockchain APIs.\nPerform smart contract testing.\nEnsure blockchain security.\n\nRequired Skills\nSolidity\nEthereum\nHardhat\nRemix\nWeb3.js\nEthers.js\nJavaScript\nGit\n\nPreferred Skills\nAvalanche\nPolygon\nHyperledger\n\nExperience\n\n1â€“3 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nBlockchain, Solidity, Ethereum, Smart Contracts, Web3, Hardhat",
    },
    {
        'id': 'iot-engineer',
        'title': 'IoT Engineer',
        'description': "Job Summary\n\nWe are looking for an IoT Engineer to design and develop smart connected systems using embedded devices and cloud platforms.\n\nResponsibilities\nDevelop embedded software.\nInterface sensors and actuators.\nBuild IoT communication systems.\nIntegrate cloud platforms.\nMonitor IoT devices.\n\nRequired Skills\nArduino\nESP32\nRaspberry Pi\nMQTT\nPython\nC\nC++\nEmbedded Systems\nIoT Protocols\n\nPreferred Skills\nAWS IoT\nNode-RED\n\nExperience\n\n0â€“3 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nIoT, Arduino, ESP32, MQTT, Raspberry Pi, Embedded Systems",
    },
    {
        'id': 'dba',
        'title': 'Database Administrator (DBA)',
        'description': "Job Summary\n\nWe are seeking a Database Administrator to manage, optimize, and secure enterprise database systems.\n\nResponsibilities\nInstall and configure databases.\nMonitor database performance.\nPerform backup and recovery.\nOptimize SQL queries.\nEnsure data security.\n\nRequired Skills\nMySQL\nPostgreSQL\nOracle\nSQL Server\nSQL\nBackup & Recovery\nPerformance Tuning\nLinux\n\nPreferred Skills\nMongoDB\nRedis\n\nExperience\n\n2â€“5 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nDatabase Administrator, MySQL, PostgreSQL, Oracle, SQL",
    },
    {
        'id': 'sysadmin',
        'title': 'System Administrator',
        'description': "Job Summary\n\nWe are hiring a System Administrator responsible for maintaining servers, operating systems, and enterprise IT infrastructure.\n\nResponsibilities\nConfigure servers.\nManage user accounts.\nMonitor system health.\nPerform software updates.\nTroubleshoot infrastructure issues.\n\nRequired Skills\nLinux\nWindows Server\nActive Directory\nBash\nPowerShell\nNetworking\nVirtualization\nVMware\n\nPreferred Skills\nDocker\nAnsible\n\nExperience\n\n1â€“4 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nLinux, Windows Server, Active Directory, System Administration",
    },
    {
        'id': 'mlops',
        'title': 'MLOps Engineer',
        'description': "Job Summary\n\nWe are looking for an MLOps Engineer to automate machine learning workflows and deploy scalable ML solutions.\n\nResponsibilities\nDeploy ML models.\nAutomate ML pipelines.\nMonitor model performance.\nManage model versioning.\nCollaborate with ML engineers.\n\nRequired Skills\nPython\nMLflow\nDocker\nKubernetes\nAirflow\nGit\nAWS SageMaker\nAzure ML\nVertex AI\nCI/CD\n\nPreferred Skills\nKubeflow\nTerraform\n\nExperience\n\n2â€“5 Years\n\nEducation\n\nBachelor's or Master's Degree.\n\nATS Keywords\n\nMLOps, MLflow, Kubeflow, Docker, Kubernetes, SageMaker",
    },
    {
        'id': 'sre',
        'title': 'Site Reliability Engineer (SRE)',
        'description': "Job Summary\n\nWe are seeking a Site Reliability Engineer to ensure system reliability, scalability, and high availability across production environments.\n\nResponsibilities\nMonitor production systems.\nAutomate operational tasks.\nImprove system reliability.\nPerform incident response.\nOptimize infrastructure performance.\n\nRequired Skills\nLinux\nDocker\nKubernetes\nPrometheus\nGrafana\nTerraform\nAWS\nBash\nGit\nCI/CD\n\nPreferred Skills\nGo\nPython\nAnsible\n\nExperience\n\n2â€“5 Years\n\nEducation\n\nBachelor's Degree.\n\n    ATS Keywords\n\nSRE, Kubernetes, Docker, Prometheus, Grafana, Terraform, AWS",
    },
    {
        'id': 'ai-research',
        'title': 'AI Research Engineer',
        'description': "Job Summary\n\nWe are looking for an AI Research Engineer to develop cutting-edge artificial intelligence models and contribute to research-driven innovations in machine learning and deep learning.\n\nResponsibilities\nResearch and implement state-of-the-art AI models.\nTrain and fine-tune deep learning architectures.\nRead and reproduce research papers.\nOptimize model performance.\nCollaborate with engineering teams for deployment.\n\nRequired Skills\nPython\nPyTorch\nTensorFlow\nDeep Learning\nTransformers\nComputer Vision\nNLP\nCUDA\nGit\nLinux\n\nPreferred Skills\nHugging Face\nDistributed Training\nJAX\nMLflow\n\nExperience\n\n2â€“5 Years\n\nEducation\n\nMaster's or Bachelor's in Computer Science, Artificial Intelligence, or related field.\n\nATS Keywords\n\nAI Research, Deep Learning, Transformers, PyTorch, TensorFlow, CUDA",
    },
    {
        'id': 'prompt-engineer',
        'title': 'Prompt Engineer',
        'description': "Job Summary\n\nWe are seeking a Prompt Engineer to design, evaluate, and optimize prompts for Large Language Models while building AI-powered applications.\n\nResponsibilities\nDesign effective prompts.\nEvaluate LLM responses.\nBuild prompt pipelines.\nOptimize AI workflows.\nCollaborate with AI engineers.\n\nRequired Skills\nPrompt Engineering\nOpenAI API\nGemini API\nClaude API\nLangChain\nLangGraph\nPython\nRAG\nVector Databases\nGit\n\nPreferred Skills\nMCP\nLlamaIndex\nPrompt Evaluation\n\nExperience\n\n0â€“3 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nPrompt Engineering, LLM, LangChain, OpenAI, Gemini, Claude, RAG",
    },
    {
        'id': 'robotics',
        'title': 'Robotics Engineer',
        'description': "Job Summary\n\nWe are looking for a Robotics Engineer to develop intelligent robotic systems integrating hardware, software, and computer vision technologies.\n\nResponsibilities\nDevelop robotic applications.\nIntegrate sensors.\nBuild autonomous navigation systems.\nImplement computer vision algorithms.\nTest robotic systems.\n\nRequired Skills\nROS\nPython\nC++\nOpenCV\nSLAM\nEmbedded Systems\nSensors\nLinux\n\nPreferred Skills\nGazebo\nNVIDIA Jetson\n\nExperience\n\n1â€“4 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nRobotics, ROS, OpenCV, SLAM, Sensors, Embedded Systems",
    },
    {
        'id': 'ar-vr-dev',
        'title': 'AR/VR Developer',
        'description': "Job Summary\n\nWe are seeking an AR/VR Developer to build immersive augmented and virtual reality applications for mobile and desktop platforms.\n\nResponsibilities\nDevelop AR/VR applications.\nBuild interactive 3D environments.\nOptimize rendering performance.\nIntegrate sensors and controllers.\n\nRequired Skills\nUnity\nUnreal Engine\nC#\nC++\nARCore\nARKit\n3D Graphics\nGit\n\nPreferred Skills\nBlender\nOculus SDK\n\nExperience\n\n1â€“3 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nAR, VR, Unity, Unreal Engine, ARCore, ARKit",
    },
    {
        'id': 'big-data',
        'title': 'Big Data Engineer',
        'description': "Job Summary\n\nWe are looking for a Big Data Engineer to design and maintain large-scale distributed data processing systems.\n\nResponsibilities\nBuild ETL pipelines.\nProcess large datasets.\nOptimize distributed systems.\nMaintain data lakes.\nEnsure data quality.\n\nRequired Skills\nApache Spark\nHadoop\nKafka\nHive\nScala\nPython\nSQL\nDatabricks\n\nPreferred Skills\nSnowflake\nAirflow\nAWS\n\nExperience\n\n2â€“5 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nBig Data, Spark, Kafka, Hadoop, Databricks, ETL",
    },
    {
        'id': 'tech-writer',
        'title': 'Technical Writer',
        'description': "Job Summary\n\nWe are looking for a Technical Writer to create high-quality technical documentation, API references, user guides, and developer documentation.\n\nResponsibilities\nWrite technical documentation.\nMaintain API documentation.\nCreate tutorials and guides.\nCollaborate with engineering teams.\nUpdate documentation regularly.\n\nRequired Skills\nMarkdown\nGit\nAPI Documentation\nOpenAPI\nSwagger\nTechnical Writing\n\nPreferred Skills\nDocusaurus\nReadTheDocs\n\nExperience\n\n0â€“3 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nTechnical Writing, API Documentation, Markdown, Swagger, OpenAPI",
    },
    {
        'id': 'salesforce',
        'title': 'Salesforce Developer',
        'description': "Job Summary\n\nWe are seeking a Salesforce Developer to customize Salesforce CRM solutions and develop scalable enterprise applications.\n\nResponsibilities\nDevelop Salesforce applications.\nCustomize CRM workflows.\nBuild Lightning components.\nIntegrate third-party APIs.\nMaintain Salesforce platform.\n\nRequired Skills\nSalesforce\nApex\nLightning Web Components\nSOQL\nJavaScript\nREST APIs\nGit\n\nPreferred Skills\nSalesforce Certifications\nVisualforce\n\nExperience\n\n1â€“4 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nSalesforce, Apex, Lightning, CRM, SOQL",
    },
    {
        'id': 'sap-consultant',
        'title': 'SAP Consultant',
        'description': "Job Summary\n\nWe are looking for an SAP Consultant to implement, configure, and optimize SAP solutions for enterprise clients.\n\nResponsibilities\nConfigure SAP modules.\nAnalyze business requirements.\nSupport SAP implementations.\nTroubleshoot SAP issues.\nTrain end users.\n\nRequired Skills\nSAP\nSAP HANA\nABAP\nERP\nSQL\nBusiness Process Analysis\n\nPreferred Skills\nSAP Fiori\nSAP S/4HANA\n\nExperience\n\n2â€“5 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nSAP, SAP HANA, ABAP, ERP, SAP Consultant",
    },
    {
        'id': 'bi-engineer',
        'title': 'Business Intelligence (BI) Engineer',
        'description': "Job Summary\n\nWe are seeking a Business Intelligence Engineer to design dashboards, analyze business data, and support data-driven decision-making.\n\nResponsibilities\nDevelop dashboards.\nBuild data pipelines.\nWrite SQL queries.\nAnalyze business trends.\nPresent actionable insights.\n\nRequired Skills\nPower BI\nTableau\nSQL\nExcel\nPython\nETL\nData Warehousing\n\nPreferred Skills\nSnowflake\nAzure Data Factory\n\nExperience\n\n1â€“4 Years\n\nEducation\n\nBachelor's Degree.\n\nATS Keywords\n\nPower BI, Tableau, SQL, ETL, Business Intelligence, Data Warehouse",
    },
    {
        'id': 'product-manager',
        'title': 'Product Manager',
        'description': "Job Summary\n\nWe are looking for a Product Manager to define product strategy, gather requirements, and collaborate with engineering and design teams to deliver high-quality software products.\n\nResponsibilities\nDefine product roadmap.\nGather business requirements.\nPrioritize product features.\nWork with cross-functional teams.\nAnalyze customer feedback.\nTrack product success metrics.\n\nRequired Skills\nProduct Management\nAgile\nScrum\nJira\nProduct Roadmapping\nUser Stories\nStakeholder Management\nData Analysis\nCommunication\n\nPreferred Skills\nSQL\nFigma\nA/B Testing\nProduct Analytics\n\nExperience\n\n2â€“5 Years\n\nEducation\n\nBachelor's Degree in Computer Science, Business, or related field.\n\nATS Keywords\n\nProduct Manager, Agile, Scrum, Jira, Roadmap, User Stories, Product Strategy",
    },
]
