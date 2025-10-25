# interview_data.py

# --- Categories for the UI Form ---
LEVEL_CATEGORIES = ["B.Tech", "M.Tech", "Degree"]
BRANCH_CATEGORIES = [
    "CSE", "CSD-DS", "AI/ML", "Cyber Security", "IOT", "IT", 
    "EEE", "ECE", "MECH", "CIVIL", "ECM", "CSM"
]
ROLE_CATEGORIES = [
    "Data Scientist", "AI/ML Engineer", "LLM Developer", 
    "Java Developer", "Python Developer", "DevOps Engineer"
]

# --- Universal Introduction Questions ---
PHASE_INTRODUCTION_Q = [
    {"text": "Walk me through your background and career story as it relates to this role.", "concept": "introduction_icebreaker", "difficulty": "easy"},
    {"text": "What specifically interests you about this role, and why did you choose to apply to our company?", "concept": "motivation_fit", "difficulty": "easy"},
]

# --- Universal Soft Skill / Behavioral Questions ---
PHASE_SOFT_SKILL_Q = [
    {"text": "Describe a time you had to meet a demanding deadline under significant pressure. How did you manage your time?", "concept": "skill_time_management", "difficulty": "medium"},
    {"text": "Tell me about a project failure or a major mistake you made. How did you handle the stress and what did you learn?", "concept": "skill_stress_management", "difficulty": "medium"},
    {"text": "Describe a situation where you had to lead a task or a small group. What was your leadership style?", "concept": "skill_leadership", "difficulty": "medium"},
    {"text": "Give an example of a time you received constructive criticism. How did you process it and apply the feedback?", "concept": "skill_communication", "difficulty": "medium"},
    {"text": "Describe a conflict you had with a team member. How did you resolve the disagreement to reach a group consensus?", "concept": "skill_group_discussion", "difficulty": "hard"},
    {"text": "How do you prioritize competing demands or tasks when you have multiple deadlines looming?", "concept": "skill_prioritization", "difficulty": "hard"},
    {"text": "What are your professional weaknesses, and what steps are you taking to improve them?", "concept": "skill_self_awareness", "difficulty": "easy"},
    {"text": "How do you gauge whether a day at work was successful or not?", "concept": "skill_work_ethic", "difficulty": "easy"},
]

# --- 1. Comprehensive Interview Question Bank (Indexed by Role) ---
INTERVIEW_QUESTIONS_BY_ROLE = {
    "Data Scientist": [
        {"text": "Explain the difference between supervised and unsupervised learning.", "concept": "ml_basics", "difficulty": "easy"},
        {"text": "Explain the concepts of Precision, Recall, and F1-Score. Which metric would you prioritize when diagnosing a rare disease?", "concept": "ml_metrics", "difficulty": "medium"},
        {"text": "How do you detect and treat multicollinearity in a regression model?", "concept": "stats_regression", "difficulty": "medium"},
        {"text": "How does Principal Component Analysis (PCA) work, and when should you avoid using it?", "concept": "dimensionality_reduction", "difficulty": "hard"},
        {"text": "Explain the difference between bagging and boosting methods.", "concept": "ensemble_methods", "difficulty": "hard"},
    ],
    "AI/ML Engineer": [
        {"text": "Explain the bias-variance tradeoff and provide a practical example of a model exhibiting high variance.", "concept": "ml_bias_variance", "difficulty": "medium"},
        {"text": "What is a vanishing gradient problem, and what mechanisms can be used to mitigate it?", "concept": "deep_learning_fix", "difficulty": "medium"},
        {"text": "Walk through the architecture of a Convolutional Neural Network (CNN).", "concept": "nn_architecture", "difficulty": "medium"},
        {"text": "Explain the purpose of batch normalization and where it is typically applied in a network.", "concept": "nn_optimization", "difficulty": "hard"},
        {"text": "Discuss the trade-offs of using different activation functions (ReLU, Sigmoid, Tanh).", "concept": "nn_activation", "difficulty": "hard"},
    ],
    "LLM Developer": [
        {"text": "Describe the difference between fine-tuning and prompt engineering.", "concept": "llm_techniques", "difficulty": "medium"},
        {"text": "Explain the transformer architecture's self-attention mechanism, focusing on Query, Key, and Value vectors.", "concept": "llm_architecture", "difficulty": "medium"},
        {"text": "What is Retrieval-Augmented Generation (RAG)?", "concept": "rag_concepts", "difficulty": "medium"},
        {"text": "Discuss the potential security risks associated with prompt injection attacks and how to prevent them.", "concept": "llm_security", "difficulty": "hard"},
        {"text": "Describe the process of pre-training a large language model like GPT or BERT.", "concept": "llm_training", "difficulty": "hard"},
    ],
    "Java Developer": [
        {"text": "Explain the concept of encapsulation and why it is a fundamental pillar of OOP.", "concept": "java_oop", "difficulty": "easy"},
        {"text": "Differentiate between `HashMap` and `TreeMap` in Java Collections Framework.", "concept": "java_collections", "difficulty": "medium"},
        {"text": "What is the purpose of the 'finally' block in a try-catch-finally statement, and when is it executed?", "concept": "java_exceptions", "difficulty": "medium"},
        {"text": "Explain the concept of Immutable objects in Java. List their key benefits.", "concept": "java_immutable", "difficulty": "hard"},
        {"text": "What is the distinction between checked, unchecked, and error exceptions?", "concept": "java_exceptions_hard", "difficulty": "hard"},
    ],
    "Python Developer": [
        {"text": "What is the Python GIL, and how does it affect multi-threading?", "concept": "python_gil", "difficulty": "medium"},
        {"text": "Explain Python decorators. Give an example of how you would use one.", "concept": "python_decorators", "difficulty": "medium"},
        {"text": "Differentiate between `list`, `tuple`, `set`, and `dictionary`.", "concept": "python_data_structures", "difficulty": "easy"},
        {"text": "How do context managers work in Python? Write a simple example using the `with` statement.", "concept": "python_context_manager", "difficulty": "hard"},
        {"text": "What are generators and iterators? When should you use a generator?", "concept": "python_generators", "difficulty": "hard"},
    ],
    "DevOps Engineer": [
        {"text": "What is a Docker image, and what are the main advantages of using containers over traditional VMs?", "concept": "containerization", "difficulty": "medium"},
        {"text": "Describe the difference between CI, CD, and Continuous Deployment.", "concept": "devops_ci_cd", "difficulty": "medium"},
        {"text": "Explain what a Kubernetes service is and differentiate between NodePort and LoadBalancer types.", "concept": "k8s_networking", "difficulty": "medium"},
        {"text": "How would you implement a blue/green deployment strategy using a CI/CD pipeline?", "concept": "devops_deployment_hard", "difficulty": "hard"},
        {"text": "Design a highly available and scalable monitoring stack for a microservices architecture.", "concept": "devops_monitoring", "difficulty": "hard"},
    ]
}

# --- 2. Pre-Curated Remedial Resources (Must be a top-level dictionary) ---
# interview_data.py (Replace the Remedial Resources section)

# --- 2. Pre-Curated Remedial Resources (Must be a top-level dictionary) ---
REMEDIAL_RESOURCES = {
    "communication_star": {"title": "Mastering Behavioral Questions with the STAR Method", "link": "https://www.mindtools.com/aq2c9y8/star-method"},
    "ml_metrics": {"title": "Precision, Recall, and F1-Score Explained", "link": "https://www.coursera.org/courses/ml-metrics-guide"},
    "stats_regression": {"title": "Multicollinearity: Detection and Treatment", "link": "https://www.towardsdatascience.com/multicollinearity-in-linear-regression"},
    "experimentation": {"title": "A/B Testing and Statistical Significance", "link": "https://www.optimizely.com/optimization-glossary/ab-testing/"},
    "ml_bias_variance": {"title": "Bias-Variance Tradeoff Deep Dive", "link": "https://www.edx.org/course/ml-bias-variance"},
    "deep_learning_fix": {"title": "Vanishing Gradient Problem and Solutions", "link": "https://www.deeplearningbook.org/"},
    "llm_architecture": {"title": "The Transformer Model Explained (Self-Attention)", "link": "https://www.youtube.com/watch?v=transformer_architecture"},
    "rag_concepts": {"title": "Retrieval-Augmented Generation (RAG) Basics", "link": "https://www.pinecone.io/learn/retrieval-augmented-generation/"},
    "java_oop": {"title": "Java Encapsulation and Abstraction", "link": "https://docs.oracle.com/javase/tutorial/java/concepts/"},
    "python_gil": {"title": "Understanding Python's Global Interpreter Lock (GIL)", "link": "https://realpython.com/python-gil/"},
    "containerization": {"title": "Docker Official Documentation: Images vs Containers", "link": "https://docs.docker.com/get-started/overview/"},
    "devops_ci_cd": {"title": "CI/CD Pipeline Fundamentals", "link": "https://about.gitlab.com/topics/ci-cd/"},
    "k8s_networking": {"title": "Kubernetes Service Types Explained", "link": "https://kubernetes.io/docs/concepts/services-networking/service/"},
    "communication_structure": {"title": "Improving Clarity in Technical Explanations", "link": "https://www.coursera.org/courses/communication-skills"},
    "filler_words": {"title": "Video: Eliminate 'Um' and 'Like' from Your Speech", "link": "https://www.youtube.com/watch?v=fluency_guide"},
    "data_cleaning": {"title": "Handling Missing Data Techniques", "link": "https://www.towardsdatascience.com/missing-data-guide"},
    "stats_regression": {"title": "Detecting Multicollinearity", "link": "https://www.towardsdatascience.com/multicollinearity-in-linear-regression"},
    "ml_algorithms_easy": {"title": "Naive Bayes Intuition and Application", "link": "https://www.geeksforgeeks.org/naive-bayes-algorithm/"},
    "experimentation": {"title": "A/B Testing Best Practices", "link": "https://www.optimizely.com/optimization-glossary/ab-testing/"},
    "dimensionality_reduction": {"title": "Principal Component Analysis (PCA) Guide", "link": "https://www.datacamp.com/tutorial/principal-component-analysis"},
    "ensemble_methods": {"title": "Bagging vs. Boosting Ensemble Methods", "link": "https://www.datacamp.com/tutorial/bagging-and-boosting-in-machine-learning"},
    "learning_growth": {"title": "Deep Learning Research & Resources", "link": "https://www.paperswithcode.com/"},
    "nn_architecture": {"title": "Convolutional Neural Networks (CNN) Architecture", "link": "https://www.tensorflow.org/tutorials/images/cnn"},
    "nn_optimization": {"title": "Batch Normalization Explained", "link": "https://www.datacamp.com/tutorial/understanding-batch-normalization"},
    "nn_activation": {"title": "Choosing the Right Activation Function", "link": "https://towardsdatascience.com/activation-functions-neural-networks-1cbd9f8d91d6"},
    "coding_ml": {"title": "Implementing Logistic Regression from Scratch", "link": "https://machinelearningmastery.com/implement-logistic-regression-from-scratch-in-python/"},
    "llm_advanced": {"title": "Transformer Attention Masks Deep Dive", "link": "https://jalammar.github.io/illustrated-transformer/"},
    "llm_training": {"title": "The Pre-training Process of Large Language Models", "link": "https://arxiv.org/abs/2005.14165"},
    "java_exceptions_hard": {"title": "Checked vs Unchecked Exceptions in Java", "link": "https://docs.oracle.com/javase/tutorial/essential/exceptions/runtime.html"},
    "java_collections": {"title": "Difference between HashMap and TreeMap", "link": "https://www.geeksforgeeks.org/difference-between-hashmap-and-treemap-in-java/"},
    "java_multithreading": {"title": "Java Thread Lifecycle States", "link": "https://docs.oracle.com/javase/8/docs/api/java/lang/Thread.State.html"},
    "java_immutable": {"title": "Creating Immutable Objects in Java", "link": "https://www.javatpoint.com/immutable-object"},
    "coding_java": {"title": "Reverse a String without Library Functions (Java)", "link": "https://www.geeksforgeeks.org/java-program-to-reverse-a-string/"},
    "python_decorators": {"title": "Python Decorators Explained", "link": "https://realpython.com/primer-on-python-decorators/"},
    "python_data_structures": {"title": "List, Tuple, Set, Dictionary Comparison", "link": "https://www.w3schools.com/python/python_dictionaries.asp"},
    "python_oop_mro": {"title": "Method Resolution Order (MRO) in Python", "link": "https://www.python.org/dev/peps/pep-0441/"},
    "python_context_manager": {"title": "Python Context Managers (`with` statement)", "link": "https://realpython.com/python-with-statement/"},
    "python_generators": {"title": "Generators vs Iterators in Python", "link": "https://realpython.com/introduction-to-python-generators/"},
    "coding_python": {"title": "Find First Non-Repeating Character (Python)", "link": "https://www.geeksforgeeks.org/python-program-to-find-first-non-repeating-character/"},
    "devops_iac": {"title": "Infrastructure as Code (IaC) Fundamentals", "link": "https://aws.amazon.com/devops/what-is-iac/"},
    "network_flow": {"title": "Kubernetes Request Lifecycle Deep Dive", "link": "https://learnk8s.io/kubernetes-network-policy"},
    "devops_deployment_hard": {"title": "Blue/Green Deployment Strategy", "link": "https://martinfowler.com/bliki/BlueGreenDeployment.html"},
    "devops_monitoring": {"title": "Microservices Monitoring Stack Design", "link": "https://prometheus.io/docs/introduction/overview/"},
    "skill_time_management": {"title": "Techniques for Managing Time and Deadlines", "link": "https://www.mindtools.com/pages/article/newHTE_04.htm"},
    "skill_stress_management": {"title": "How to Handle Stress and Pressure at Work", "link": "https://www.verywellmind.com/stress-management-techniques-2358055"},
    "skill_leadership": {"title": "Developing Your Leadership Style", "link": "https://www.coursera.org/learn/leadership-development"},
    "skill_communication": {"title": "Receiving and Applying Constructive Criticism", "link": "https://hbr.org/2016/01/how-to-respond-to-constructive-criticism"},
    "skill_group_discussion": {"title": "Resolving Conflict in Team Environments", "link": "https://www.pon.harvard.edu/daily/conflict-resolution/conflict-resolution-techniques/"},
    "skill_prioritization": {"title": "Prioritization Matrices and Techniques", "link": "https://www.mindtools.com/pages/article/newHTE_07.htm"},
    "skill_self_awareness": {"title": "Identifying Professional Strengths and Weaknesses", "link": "https://www.forbes.com/sites/forbescoachescouncil/2019/04/01/how-to-identify-your-strengths-and-weaknesses/"},
    "skill_work_ethic": {"title": "Measuring and Improving Work Ethic", "link": "https://www.themuse.com/advice/how-to-measure-your-productivity"},
}