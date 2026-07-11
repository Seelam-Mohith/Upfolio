import re

# ---------------------------------------------------------------------------
# Contact-information regex patterns
# ---------------------------------------------------------------------------

EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
)

PHONE_PATTERN = re.compile(
    r"(?:\+?\d{1,3}[\s\-]?)?"           # optional country code
    r"(?:\(?\d{2,4}\)?[\s\-]?)?"         # optional area code
    r"\d{3,4}[\s\-]?\d{3,4}",            # main number
)

LINKEDIN_PATTERN = re.compile(
    r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9\-_%]+/?",
    re.IGNORECASE,
)

GITHUB_PATTERN = re.compile(
    r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9\-_%]+/?",
    re.IGNORECASE,
)

PORTFOLIO_PATTERN = re.compile(
    r"(?:https?://)?(?:www\.)?[a-zA-Z0-9\-]+(?:\.[a-zA-Z]{2,})+(?:/[^\s,;]*)?",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Section-heading detection
# ---------------------------------------------------------------------------

# Common resume section headings — matched case-insensitively on a full line.
SECTION_HEADINGS: list[str] = [
    "summary",
    "profile",
    "objective",
    "about",
    "about me",
    "contact",
    "contact information",
    "personal information",
    "skills",
    "technical skills",
    "tech stack",
    "technologies",
    "programming languages",
    "tools and technologies",
    "experience",
    "work experience",
    "professional experience",
    "employment history",
    "internships",
    "internship experience",
    "projects",
    "personal projects",
    "key projects",
    "notable projects",
    "education",
    "academic background",
    "certifications",
    "certificates",
    "licenses",
    "achievements",
    "awards",
    "honors",
    "extracurricular",
    "publications",
    "references",
    "languages",
    "volunteer",
    "volunteer experience",
]

# Build a single regex that matches any of the headings on its own line.
_SECTION_PATTERN = re.compile(
    r"^\s*(" + "|".join(re.escape(h) for h in SECTION_HEADINGS) + r")\s*[:\-=]?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

# Pattern for lines that look like section headers but are NOT in the known
# list — heuristic: short, all-uppercase or Title Case, followed by a newline.
_GENERIC_HEADER = re.compile(
    r"^\s*[A-Z][A-Za-z /&]{2,40}\s*$",
    re.MULTILINE,
)

# ---------------------------------------------------------------------------
# Education extraction helpers
# ---------------------------------------------------------------------------

# Matches common degree strings: B.Tech, B.S., M.S., MBA, Ph.D, etc.
DEGREE_PATTERN = re.compile(
    r"(?:B\.?Tech(?:nology)?|B\.?S\.?|B\.?A\.?|B\.?E\.?|B\.?C\.?A?"
    r"|M\.?Tech(?:nology)?|M\.?S\.?|M\.?A\.?|M\.?B\.?A?|M\.?C\.?A?"
    r"|Ph\.?D\.?|Doctorate|Bachelor(?:'s)?|Master(?:'s)?|Associate(?:'s)?)"
    r"(?:\s+(?:of|in|in\s+))?[\w\s]{0,40}",
    re.IGNORECASE,
)

# CGPA / GPA pattern
CGPA_PATTERN = re.compile(
    r"(?:CGPA|GPA|Percentage|Percent|Score)\s*[:=\-]?\s*(\d+(?:\.\d+)?)\s*(?:/\s*(?:10|100))?",
    re.IGNORECASE,
)

# Graduation year — 4-digit year between 1980 and 2035
YEAR_PATTERN = re.compile(
    r"(?:20[0-2]\d|19[89]\d)",
)

# College / university keywords that signal the start of a college name
COLLEGE_KEYWORDS = re.compile(
    r"(?:University|College|Institute|School|Academy|Centre|Center|Polytechnic)",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Experience extraction helpers
# ---------------------------------------------------------------------------

# Date-range patterns commonly found in resumes.
# e.g. "Jan 2022 - Present", "2020 - 2023", "06/2021 – 12/2023"
DATE_RANGE_PATTERN = re.compile(
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?"
    r"|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?"
    r"|Dec(?:ember)?)"
    r"\s+\d{4}"
    r"\s*[\-–—to]+\s*"
    r"(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?"
    r"|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?"
    r"|Dec(?:ember)?)\s+\d{4}|Present|Current|Now)",
    re.IGNORECASE,
)

# Simpler year-range: "2020 - 2023" or "2020 – Present"
YEAR_RANGE_PATTERN = re.compile(
    r"(?:19|20)\d{2}\s*[\-–—to]+\s*(?:(?:19|20)\d{2}|Present|Current|Now)",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Project extraction helpers
# ---------------------------------------------------------------------------

# A line that starts with a bullet or dash followed by a project-like title
PROJECT_BULLET_PATTERN = re.compile(
    r"^[\s]*[•\-\*\►\▹]\s*(.+)",
    re.MULTILINE,
)

# Technology list in parentheses, e.g. "(Python, Flask, PostgreSQL)"
TECH_LIST_PATTERN = re.compile(
    r"\(([^)]+)\)",
)

# Technology list after a separator, e.g. "Technologies: Python, Flask"
TECH_COLON_PATTERN = re.compile(
    r"(?:Technologies?|Tech\s*Stack|Tools?|Built\s+with|Using)\s*[:=\-]\s*(.+)",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Configurable skills database
# ---------------------------------------------------------------------------

SKILLS_DB: dict[str, list[str]] = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#",
        "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R",
        "MATLAB", "Perl", "Lua", "Dart", "Elixir", "Haskell", "Clojure",
        "F#", "Objective-C", "Assembly", "SQL", "Shell", "Bash",
        "PowerShell", "Groovy", "Julia", "Fortran", "COBOL", "Pascal",
        "Ada", "Solidity", "VHDL", "Verilog", "WebAssembly",
    ],
    "Frontend Frameworks & Libraries": [
        "React", "React.js", "ReactJS", "Angular", "AngularJS",
        "Vue.js", "Vue", "VueJS", "Next.js", "NextJS", "Nuxt.js", "NuxtJS",
        "Svelte", "SvelteKit", "Remix", "Gatsby", "Astro", "SolidJS", "Qwik",
        "jQuery", "Backbone.js", "Ember.js", "Lit", "Stencil",
        "Tailwind CSS", "Tailwind", "Bootstrap", "Material UI", "MUI",
        "Chakra UI", "Ant Design", "Styled Components", "Emotion",
        "Redux", "Zustand", "Recoil", "MobX", "Vuex", "Pinia",
        "D3.js", "Three.js", "Chart.js", "Recharts", "Framer Motion",
        "Framer", "React Spring", "GSAP",
    ],
    "Backend Frameworks": [
        "Django", "Django REST Framework", "DRF", "Flask", "FastAPI",
        "Express.js", "Express", "NestJS", "NestJS", "Spring Boot",
        "Spring", "Spring MVC", "Ruby on Rails", "Rails", "Sinatra",
        "Laravel", "Symfony", "CodeIgniter", "ASP.NET", "ASP.NET Core",
        "Gin", "Echo", "Fiber", "Actix", "Rocket", "Axum",
        "Phoenix", "Slim", "Koa", "Hapi", "Fastify",
        "Strapi", "Hasura", "Supabase",
    ],
    "Databases": [
        "MySQL", "PostgreSQL", "Postgres", "MongoDB", "Redis",
        "Elasticsearch", "SQLite", "MariaDB", "DynamoDB", "Cassandra",
        "Neo4j", "Firebase Firestore", "Firestore", "CouchDB",
        "RethinkDB", "TimescaleDB", "InfluxDB", "ClickHouse",
        "PlanetScale", "Cosmos DB", "Couchbase", "Memcached",
        "Amazon RDS", "Amazon DynamoDB", "Google Firestore",
        "Microsoft SQL Server", "MSSQL", "Oracle DB", "DB2",
        "Prisma", "Sequelize", "TypeORM", "Mongoose", "SQLAlchemy",
        "Alembic", "Flyway",
    ],
    "Cloud Platforms": [
        "AWS", "Amazon Web Services", "Google Cloud Platform", "GCP",
        "Microsoft Azure", "Azure", "Heroku", "Netlify", "Vercel",
        "DigitalOcean", "Linode", "Cloudflare", "Render", "Fly.io",
        "Railway", "OpenShift", "Firebase", "Supabase",
        "AWS Lambda", "AWS EC2", "AWS S3", "AWS ECS", "AWS EKS",
        "AWS RDS", "AWS SQS", "AWS SNS", "AWS CloudFront",
        "Google Compute Engine", "Google Kubernetes Engine", "GKE",
        "Google Cloud Functions", "Google Cloud Run",
        "Azure Functions", "Azure DevOps", "Azure Blob Storage",
    ],
    "DevOps & Infrastructure": [
        "Docker", "Kubernetes", "K8s", "Jenkins", "GitHub Actions",
        "GitLab CI", "GitLab CI/CD", "Travis CI", "CircleCI",
        "Ansible", "Terraform", "Pulumi", "Chef", "Puppet",
        "Nginx", "Apache", "Apache Kafka", "Grafana", "Prometheus",
        "Datadog", "Splunk", "ELK Stack", "Elastic Stack",
        "ArgoCD", "Helm", "Vagrant", "Packer",
        "Linux", "Ubuntu", "CentOS", "Debian", "Alpine Linux",
        "VMware", "VirtualBox", "Bamboo", "TeamCity",
    ],
    "AI/ML Tools": [
        "TensorFlow", "PyTorch", "Keras", "scikit-learn", "Scikit-learn",
        "NumPy", "Pandas", "Matplotlib", "Seaborn", "Plotly",
        "OpenCV", "NLTK", "spaCy", "Hugging Face", "Transformers",
        "LangChain", "LlamaIndex", "MLflow", "Weights & Biases", "W&B",
        "XGBoost", "LightGBM", "CatBoost", "JAX", "ONNX",
        "CUDA", "cuDNN", "TensorRT", "OpenAI API", "Anthropic API",
        "Stable Diffusion", "GAN", "GANs", "BERT", "GPT", "LLaMA",
        "Mistral", "RAG", "Vector Database", "Pinecone", "ChromaDB",
        "Weaviate", "Milvus", "FAISS", "DeepSpeed", "Ray",
        "Apache Spark", "Spark MLlib", "Databricks", "Hadoop",
        "Airflow", "dbt", "Kubeflow", "Seldon", "BentoML",
        "Neural Networks", "CNN", "RNN", "LSTM", "Transformer",
        "Reinforcement Learning", "NLP", "Computer Vision",
        "Image Processing", "Object Detection", "Semantic Segmentation",
    ],
    "Mobile Development": [
        "React Native", "Flutter", "Dart", "Swift", "SwiftUI",
        "Kotlin", "Jetpack Compose", "Xamarin", "Ionic", "Cordova",
        "PhoneGap", "Expo", "NativeScript", "Android SDK", "iOS SDK",
        "Xcode", "Android Studio", "Capacitor", "KMP",
    ],
    "Web Technologies": [
        "HTML5", "HTML", "CSS3", "CSS", "SASS", "SCSS", "Less",
        "REST API", "RESTful", "REST", "GraphQL", "gRPC", "WebSocket",
        "OAuth", "JWT", "SAML", "WebAssembly", "WebRTC",
        "Progressive Web Apps", "PWA", "SSR", "CSR", "SPA",
        "XML", "JSON", "YAML", "TCP/IP", "DNS", "HTTP/HTTPS",
        "CDN", "Load Balancing", "Microservices", "Monolith",
        "Serverless", "Edge Computing",
    ],
    "Testing": [
        "Jest", "Mocha", "Chai", "Cypress", "Playwright", "Selenium",
        "Pytest", "pytest", "JUnit", "TestNG", "xUnit", "NUnit",
        "RSpec", "PHPUnit", "Postman", "JMeter", "K6",
        "Puppeteer", "Storybook", "Enzyme", "React Testing Library",
        "Vitest", "Supertest", "Mockito", "WireMock",
        "TDD", "BDD", "Unit Testing", "Integration Testing",
        "End-to-End Testing", "E2E", "Load Testing", "Stress Testing",
    ],
    "Version Control & Collaboration": [
        "Git", "GitHub", "GitLab", "Bitbucket", "SVN", "Perforce",
        "JIRA", "Confluence", "Notion", "Trello", "Asana",
        "Linear", "Slack", "Microsoft Teams",
    ],
    "Package Managers & Build Tools": [
        "npm", "yarn", "pnpm", "pip", "Poetry", "conda",
        "Maven", "Gradle", "NuGet", "Gem", "Bundler",
        "Homebrew", "Chocolatey", "Webpack", "Vite", "Rollup",
        "esbuild", "SWC", "Babel", "Gulp", "Grunt",
        "CMake", "Make", "MSBuild",
    ],
    "CMS & E-Commerce": [
        "WordPress", "Shopify", "WooCommerce", "Magento", "Drupal",
        "Joomla", "Contentful", "Sanity", "Prismic", "Ghost",
        "Webflow", "Squarespace", "Wix",
    ],
    "Design & Prototyping": [
        "Figma", "Adobe XD", "Sketch", "InVision", "Canva",
        "Photoshop", "Illustrator", "After Effects", "Premiere Pro",
    ],
    "Security": [
        "OWASP", "SAST", "DAST", "Penetration Testing",
        "SSL/TLS", "HTTPS", "CORS", "CSRF", "XSS",
        "Burp Suite", "Nmap", "Wireshark", "Metasploit",
        "HashiCorp Vault", "Let's Encrypt",
    ],
    "Data Engineering": [
        "Apache Spark", "Apache Kafka", "Apache Airflow", "Apache Flink",
        "Apache Hadoop", "Apache Hive", "Apache NiFi", "dbt",
        "Databricks", "Snowflake", "BigQuery", "Redshift",
        "ETL", "Data Pipeline", "Data Lake", "Data Warehouse",
        "Delta Lake", "Iceberg", "Parquet",
    ],
}
