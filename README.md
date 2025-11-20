## 📅 Day 1 — LLM 기초 및 환경 설정 (5시간)
### 1. Google Colab 실습 환경 설정

GPU 활용 설정

필수 패키지 설치

노트북 구조 및 워크플로우 소개

### 2. 로컬 LLM 설치 및 구동

Hugging Face 모델 다운로드

GGUF 기반 LLM 로컬 실행

Text Generation WebUI 또는 llamacpp 활용

### 3. Transformer 기본 개념 이해

Transformer 구조 소개

Attention 메커니즘 이해

LLM 학습 및 추론 흐름

### 4. 주요 LLM 성능 비교

Vellum LLM Leaderboard 분석

모델별 특성(속도·성능·토큰 비용 등) 비교

### 5. 실습: OpenAI / Anthropic API 사용

OpenAI GPT 계열 연결

Claude API 활용

간단한 챗봇 프롬프트 실습

## 📘 LangChain 프레임워크로 오픈소스 LLM 활용 1 (5시간 중 2.5시간)
### 1. LangChain 개요 및 활용 사례

왜 LangChain인가?

AI 에이전트, RAG, 워크플로우 자동화 사례 소개

### 2. 핵심 컴포넌트 이해

PromptTemplate

Chain

Memory

Output parser

### 3. 다양한 모델 연동 실습

OpenAI

Claude

Google Gemini

Meta Llama (HF Hub)

## 📅 Day 2 — LangChain + RAG 심화 (5시간)
### 1. RAG (Retrieval-Augmented Generation) 개념

RAG 필요성 및 구조

Retrieval 단계별 기술 요소 이해

### 2. 벡터 DB 활용 (ChromaDB, Pinecone)

임베딩 생성

컬렉션 구성

문서 검색 및 쿼리 분석

### 3. 임베딩 모델 선택 및 최적화

OpenAI / Instructor / BGE / E5 임베딩 비교

Chunking 전략

검색 성능 개선 방법

### 4. 실습: 프라이빗 AI 챗봇 구축

사내 문서를 기반으로 RAG 시스템 구축

LLM 연결 + 검증

Colab 기반 미니 웹앱 구성(Optional)

## 📅 Day 3 — 평가 & Agent 실전 구축 (5시간)
## 1. LLM 모델 평가 (3시간)
### LangSmith / RAGAs 기반 평가

LLM 애플리케이션 평가 개념

LangSmith 프로젝트 구성

RAGAs 평가 지표(Recall, MRR, Faithfulness 등)

평가 결과 기반 개선 전략

## 2. LangGraph로 만드는 AI Agent (3시간)
### 1. LangGraph 개요

LangChain + 상태 기계 기반 프레임워크

그래프 기반 워크플로우 설계 원리

### 2. 멀티스텝 AI Agent 설계

노드(Node)와 엣지(Edge) 구성

Tool 사용

루프·조건 분기 구조 만들기
