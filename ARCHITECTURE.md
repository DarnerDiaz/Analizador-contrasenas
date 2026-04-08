# Architecture & Project Structure

> **Last Updated:** April 8, 2026  
> **Version:** 2.0.0 - Enterprise-Grade Architecture

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  Streamlit Dashboard (streamlit_app.py) - Web Interface     │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              Application Logic Layer (app/)                  │
│  - Main application entry point                             │
│  - UI routing and state management                          │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│             Business Logic Layer (utils/)                    │
│  - password_analyzer.py (fortaleza & entropía)              │
│  - encryption.py (AES-256-CBC, PBKDF2)                      │
│  - patterns.py (detección de patrones)                      │
│  - pdf_generator.py (reportes)                              │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│           Data Access Layer (data/)                          │
│  - Almacenamiento cifrado local                             │
│  - Gestión de ficheros encriptados                          │
│  - Interfaz de persistencia                                 │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Core Modules

### 1. **utils/password_analyzer.py**
Análisis principal de fortaleza de contraseñas usando:
- Longitud y complejidad de caracteres
- Cálculo de entropía (usando biblioteca `zxcvbn`)
- Tiempo estimado de crack (en segundos)
- Scoring de 0-100 puntos

**Key Methods:**
```python
PasswordAnalyzer.analyze_password(pwd: str) -> dict
PasswordAnalyzer.batch_analyze(passwords: List[str]) -> List[dict]
PasswordAnalyzer.get_strength_label(score: int) -> str
```

### 2. **utils/encryption.py**
Cifrado simétrico con AES-256-CBC:
- Derivación de claves con PBKDF2-HMAC-SHA256
- 100,000 iteraciones (OWASP recommendations)
- Almacenamiento seguro de master password (salted hash)

**Key Methods:**
```python
PasswordEncryptor.encrypt(password: str, master_pwd: str) -> str
PasswordEncryptor.decrypt(encrypted: str, master_pwd: str) -> str
PasswordValidator.validate_master_password(pwd: str) -> bool
```

### 3. **utils/patterns.py**
Detección de patrones débiles:
- Fechas comunes (MM/DD/YYYY, DDMMYYYY)
- Palabras diccionario comunes
- Secuencias de teclado QWERTY
- Nombres propios
- Números secuenciales

**Key Methods:**
```python
PatternDetector.detect_patterns(password: str) -> List[str]
PatternDetector.get_pattern_recommendations(patterns: List[str]) -> List[str]
```

### 4. **utils/pdf_generator.py**
Generación de reportes en PDF:
- Análisis individual con gráficos
- Análisis masivo en batch
- Alertas visuales (rojo/verde/amarillo)
- Recomendaciones personalizadas

## 🆕 New Modules (Version 2.0.0)

### 5. **refactor/** (35 módulos)
Ejemplos de refactoring y mejora de código:
- Type hints completos usando `typing`
- Docstrings con estilo Google
- Reducción de complejidad ciclomática
- Patrones Pythonic
- Optimizaciones de rendimiento

**Use Cases:** Referencia para mejorar código existente

### 6. **security/** (35 módulos)
Auditoría de seguridad y hardening:
- Validación de entrada (@validate_input)
- Sanitización de datos
- PBKDF2 hashing (100k iterations)
- RBAC (Role-Based Access Control)
- Decoradores de autenticación (@check_authentication)

**Use Cases:** Patrones de seguridad reutilizables para nuevas funcionalidades

### 7. **performance/** (35 módulos)
Benchmarking y profiling:
- Herramientas de medición: throughput, latencia, memoria
- Uso de `time.perf_counter()` para precisión nanosecundos
- Integración con `tracemalloc` para perfilar memoria
- Stress testing frameworks

**Use Cases:** Optimización de funciones críticas de rendimiento

### 8. **advanced_tests/** (35 módulos)
Suite de testing avanzada:
- Edge cases y boundary conditions
- Concurrencia y multi-threading
- Stress testing
- Validación de integridad de datos
- Generadores de datos de prueba

**Use Cases:** Cobertura completa de casos de uso complejos

### 9. **integration/** (35 módulos)
APIs y características de integración:
- Endpoints REST
- OAuth 2.0 y JWT autenticación
- Webhook handlers
- Database adapters
- Error handling middleware
- Production-ready implementations

**Use Cases:** Integración con sistemas externos (APIs, bases de datos, servicios)

### 10. **devops/** (35 módulos YAML)
Infraestructura y deployment:
- **Kubernetes**: Deployments, Services, ConfigMaps, Ingress
- **Docker**: Configurations, builds, multi-stage builds
- **Auto-scaling**: Horizontal Pod Autoscaler (HPA)
- **CI/CD**: GitHub Actions, GitLab CI, Jenkins pipelines
- **Monitoring**: Prometheus, Grafana configurations

**Use Cases:** Deployar a producción en Kubernetes/Docker

## 🔄 Data Flow

```
User Input
    ↓
[Streamlit UI - streamlit_app.py]
    ↓
[Business Logic Layer - utils/]
    ├─→ password_analyzer.py (analyze)
    ├─→ patterns.py (detect patterns)
    ├─→ encryption.py (encrypt/decrypt)
    └─→ pdf_generator.py (generate report)
    ↓
[Data Access Layer - data/]
    ├─→ Encrypt sensitive data
    ├─→ Store locally
    └─→ Manage file system
    ↓
[Output]
    ├─→ Display in UI
    ├─→ Export PDF
    └─→ Return JSON API
```

## 🏗️ Directory Summary

| Directory | Purpose | Files | Status |
|-----------|---------|-------|--------|
| `app/` | Application entry point | main.py | Original |
| `utils/` | Core business logic | 4 main modules | Original |
| `tests/` | Original test suite | 4 test files | Original |
| `refactor/` | Code quality examples | 35 modules | NEW (v2.0.0) |
| `security/` | Security patterns | 35 modules | NEW (v2.0.0) |
| `performance/` | Benchmarking tools | 35 modules | NEW (v2.0.0) |
| `advanced_tests/` | Advanced test suite | 35 modules | NEW (v2.0.0) |
| `integration/` | API integrations | 35 modules | NEW (v2.0.0) |
| `devops/` | Infrastructure configs | 35 YAML files | NEW (v2.0.0) |
| `data/` | Data persistence | (encrypted files) | Original |
| `reports/` | Generated PDFs | *.pdf | Original |

## 🔐 Security Architecture

### Password Protection
1. **Master Password**: Salted PBKDF2-HMAC-SHA256
2. **Data Encryption**: AES-256-CBC-HMAC
3. **Key Derivation**: PBKDF2 with 100,000 iterations
4. **No External Communication**: 100% local processing

### Access Control
- Session-based authentication
- Role-based access control (RBAC)
- Rate limiting on sensitive operations
- Audit logging of operations

## 📊 Performance Considerations

### Current Optimizations
- **Streamlit Caching**: @st.cache_data for expensive computations
- **Vectorized Operations**: NumPy for batch processing
- **Database Indexing**: (future SQLite implementation)
- **Worker Pools**: Multiprocessing for parallel analysis

### Scalability
- **Current**: Single-machine, local processing
- **Future**: Distributed task queue (Celery + Redis)
- **Deployment**: Kubernetes with auto-scaling HPA

## 🧪 Testing Strategy

### Original Tests (tests/)
- Unit tests for core modules
- Coverage: 71 tests, >85% code coverage

### Advanced Tests (advanced_tests/)
- Integration tests across modules
- Stress testing and concurrency
- Edge case coverage
- Performance regression tests

## 🚀 Deployment

### Local Development
```bash
streamlit run streamlit_app.py
```

### Docker Container
```bash
docker build -t password-analyzer:v2026.1 .
docker run -p 8501:8501 password-analyzer:v2026.1
```

### Kubernetes (Production)
(See `/devops/infra_1.yaml` through `infra_35.yaml`)
```bash
kubectl apply -f devops/
kubectl port-forward svc/password-analyzer-service 8501:80
```

## 🔄 Future Architecture Plans

### v2.1.0
- SQLite local database for persistence
- Have I Been Pwned (HIBP) integration
- Password strength recommendations
- 2FA authentication

### v2.2.0
- REST API (FastAPI)
- GraphQL endpoint
- WebSocket real-time analysis
- Export to password managers (Bitwarden, 1Password)

### v3.0.0
- Microservices architecture
- Distributed caching (Redis)
- Message queue (RabbitMQ/Kafka)
- Advanced analytics and reporting
- Machine learning patterns detection

---

**Maintained by:** DarnerDiaz  
**Repository:** https://github.com/DarnerDiaz/Analizador-Fortaleza-Contrase-as  
**License:** MIT
