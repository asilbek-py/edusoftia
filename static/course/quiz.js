
document.addEventListener('DOMContentLoaded', function () {
    // DOM elements
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');
    const submitBtn = document.getElementById('submitBtn');
    const exitBtn = document.getElementById('exitBtn');
    const currentQuestionEl = document.getElementById('current-question');
    const progressFillEl = document.querySelector('.progress-fill');
    const timeDisplayEl = document.getElementById('time-display');
    const modal = document.getElementById('result-modal');
    const finalScoreEl = document.getElementById('final-score');
    const resultMessageEl = document.getElementById('result-message');
    const reviewBtn = document.getElementById('review-btn');
    const continueBtn = document.getElementById('continue-btn');

    // Quiz state
    let currentQuestion = 1;
    const totalQuestions = document.querySelectorAll('.question-block').length;
    const userAnswers = {};
    let timer;
    let timeLeft = 1800; // 30 minutes in seconds

    // Initialize quiz
    function initQuiz() {
        updateProgress();
        startTimer();

        // Add event listeners to options
        document.querySelectorAll('.option').forEach(option => {
            option.addEventListener('click', function () {
                const questionBlock = this.closest('.question-block');
                const questionId = Array.from(document.querySelectorAll('.question-block')).indexOf(questionBlock) + 1;
                const optionId = this.getAttribute('data-option');

                // Remove selected class from all options in this question
                questionBlock.querySelectorAll('.option').forEach(opt => {
                    opt.classList.remove('selected');
                });

                // Add selected class to clicked option
                this.classList.add('selected');

                // Store user answer
                userAnswers[questionId] = optionId;
            });
        });
    }

    // Update progress
    function updateProgress() {
        const progressPercent = Math.round((currentQuestion / totalQuestions) * 100);
        currentQuestionEl.textContent = currentQuestion;
        progressFillEl.style.width = `${progressPercent}%`;

        prevBtn.disabled = currentQuestion === 1;

        if (currentQuestion === totalQuestions) {
            submitBtn.style.display = 'flex';
            nextBtn.style.display = 'none';
        } else {
            submitBtn.style.display = 'none';
            nextBtn.style.display = 'flex';
        }

        // Show current question, hide others
        document.querySelectorAll('.question-block').forEach((block, index) => {
            block.style.display = (index === currentQuestion - 1) ? 'block' : 'none';
        });
    }

    // Start timer
    function startTimer() {
        clearInterval(timer);
        updateTimeDisplay();

        timer = setInterval(function () {
            timeLeft--;
            updateTimeDisplay();

            if (timeLeft <= 0) {
                clearInterval(timer);
                submitQuiz();
            }
        }, 1000);
    }

    // Update time display
    function updateTimeDisplay() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timeDisplayEl.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

        // Change color when time is running out
        if (timeLeft < 300) { // 5 minutes
            timeDisplayEl.style.color = '#ef4444';
        }
    }

    // Submit quiz
    function submitQuiz() {
        clearInterval(timer);

        // Calculate score (for demo purposes, we'll use a random score)
        const score = Math.floor(Math.random() * 40) + 60; // Random score between 60-100
        finalScoreEl.textContent = `${score}%`;

        if (score >= 80) {
            resultMessageEl.textContent = "Excellent! You have mastered this chapter.";
        } else if (score >= 60) {
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
            updateProgress();
        }
    });

    prevBtn.addEventListener('click', function () {
        if (currentQuestion > 1) {
            currentQuestion--;
            updateProgress();
        }
    });

    submitBtn.addEventListener('click', submitQuiz);

    exitBtn.addEventListener('click', function () {
        if (confirm('Are you sure you want to exit? Your progress will be lost.')) {
            window.location.href = '/'; // Redirect to home page
        }
    });

    continueBtn.addEventListener('click', function () {
        // Loading overlayni ko‘rsatamiz
        document.getElementById("redirect-loading").style.display = "flex";

        // 1 sekunddan keyin redirect
        setTimeout(function () {
            window.location.href = "/course/";
        }, 1000);
    });
    // Start the quiz
    initQuiz();
});