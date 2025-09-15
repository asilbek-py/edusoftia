document.addEventListener('DOMContentLoaded', function () {
    // DOM elements
    const nextBtn = document.querySelector('.next-btn');
    const prevBtn = document.querySelector('.prev-btn');
    const submitBtn = document.querySelector('.submit-btn');
    const currentQuestionEl = document.getElementById('current-question');
    const progressPercentEl = document.getElementById('progress-percent');
    const progressFillEl = document.querySelector('.progress-fill');
    const questionTextEl = document.getElementById('question-text');
    const timeRemainingEl = document.querySelector('.time-remaining strong');
    const modal = document.getElementById('result-modal');
    const finalScoreEl = document.getElementById('final-score');
    const resultMessageEl = document.getElementById('result-message');

    // Quiz state
    let currentQuestion = 1;
    const userAnswers = {};
    let timer;
    let timeLeft = 3600; // 1 hour in seconds

    // Savollar (real appda Django backenddan keladi)
    const questions = [
        {
            id: 1,
            text: "What is the primary focus of software evolution?",
            options: [
                { id: 1, text: "Writing new code from scratch" },
                { id: 2, text: "Maintaining and adapting existing software" },
                { id: 3, text: "Designing user interfaces" },
                { id: 4, text: "Hardware optimization" }
            ],
            correctAnswer: 2
        },
        {
            id: 2,
            text: "Which development methodology emphasizes iterative development?",
            options: [
                { id: 1, text: "Waterfall" },
                { id: 2, text: "Agile" },
                { id: 3, text: "V-Model" },
                { id: 4, text: "Big Bang" }
            ],
            correctAnswer: 2
        }
        // shu yerga qolgan savollarni qo‘shasiz...
    ];

    const totalQuestions = questions.length; // ✅ endi avtomatik

    // Initialize quiz
    function initQuiz() {
        loadQuestion(currentQuestion);
        startTimer();
    }

    // Load question
    function loadQuestion(questionNum) {
        if (questionNum > 0 && questionNum <= totalQuestions) {
            const question = questions[questionNum - 1];
            questionTextEl.textContent = question.text;

            // Update options
            const optionsContainer = document.querySelector('.options-container');
            optionsContainer.innerHTML = '';

            question.options.forEach((option, index) => {
                const optionElement = document.createElement('div');
                optionElement.className = 'option';
                optionElement.dataset.option = option.id;

                optionElement.innerHTML = `
                    <div class="option-selector">
                        <div class="option-circle"></div>
                    </div>
                    <div class="option-text">
                        <span>${String.fromCharCode(65 + index)}) ${option.text}</span>
                    </div>
                `;

                if (userAnswers[questionNum] === option.id) {
                    optionElement.classList.add('selected');
                }

                optionElement.addEventListener('click', function () {
                    selectOption(this, option.id);
                });

                optionsContainer.appendChild(optionElement);
            });

            updateProgress();
        }
    }

    // Select option
    function selectOption(optionElement, optionId) {
        document.querySelectorAll('.option').forEach(opt => {
            opt.classList.remove('selected');
        });

        optionElement.classList.add('selected');
        userAnswers[currentQuestion] = optionId;

        console.log(`User selected option ${optionId} for question ${currentQuestion}`);
    }

    // Update progress
    function updateProgress() {
        const progressPercent = Math.round((currentQuestion / totalQuestions) * 100);

        currentQuestionEl.textContent = currentQuestion;
        progressPercentEl.textContent = `${progressPercent}%`;
        progressFillEl.style.width = `${progressPercent}%`;

        prevBtn.disabled = currentQuestion === 1;
        nextBtn.disabled = currentQuestion === totalQuestions;

        if (currentQuestion === totalQuestions) {
            submitBtn.style.display = 'flex';
            nextBtn.style.display = 'none';
        } else {
            submitBtn.style.display = 'none';
            nextBtn.style.display = 'flex';
        }
    }

    // Start timer
    function startTimer() {
        clearInterval(timer);
        timer = setInterval(function () {
            timeLeft--;

            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;

            timeRemainingEl.textContent =
                `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

            if (timeLeft <= 0) {
                clearInterval(timer);
                submitQuiz();
            }
        }, 1000);
    }

    // Submit quiz
    function submitQuiz() {
        clearInterval(timer);

        let score = 0;
        for (let i = 1; i <= totalQuestions; i++) {
            if (userAnswers[i] === questions[i - 1].correctAnswer) {
                score++;
            }
        }

        const percentage = Math.round((score / totalQuestions) * 100);
        finalScoreEl.textContent = `${percentage}%`;

        if (percentage >= 80) {
            resultMessageEl.textContent = "Excellent! You have mastered this chapter.";
        } else if (percentage >= 60) {
            resultMessageEl.textContent = "Good job! You have a solid understanding.";
        } else {
            resultMessageEl.textContent = "You might want to review this chapter again.";
        }

        modal.style.display = 'flex';
    }

    // Event listeners
    nextBtn.addEventListener('click', function () {
        if (currentQuestion < totalQuestions) {
            currentQuestion++;
            loadQuestion(currentQuestion);
        }
    });

    prevBtn.addEventListener('click', function () {
        if (currentQuestion > 1) {
            currentQuestion--;
            loadQuestion(currentQuestion);
        }
    });

    submitBtn.addEventListener('click', submitQuiz);

    document.getElementById('continue-btn').addEventListener('click', function () {
        window.location.href = '/course-content/';
    });

    // Start
    initQuiz();
});
