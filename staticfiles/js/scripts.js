function handleScroll() {
    const milestones = document.querySelectorAll('.milestone');
    const employees = document.querySelectorAll('.employee');
    const farmers = document.querySelectorAll('.farmer');
    const statements = document.querySelectorAll('.statement-section');
    const triggerPoint = window.innerHeight * 0.8;

    milestones.forEach((milestone) => {
        const milestoneTop = milestone.getBoundingClientRect().top;
        if (milestoneTop < triggerPoint) {
            milestone.classList.add('visible');
        }
    });

    employees.forEach((employee) => {
        const employeeTop = employee.getBoundingClientRect().top;
        if (employeeTop < triggerPoint) {
            employee.classList.add('visible');
        }
    });

    farmers.forEach((farmer) => {
        const farmerTop = farmer.getBoundingClientRect().top;
        if (farmerTop < triggerPoint) {
            farmer.classList.add('visible');
        }
    });

    statements.forEach((statement) => {
        const statementTop = statement.getBoundingClientRect().top;
        if (statementTop < triggerPoint) {
            statement.classList.add('visible');
        }
    });
}

function handleModal() {
    const farmers = document.querySelectorAll('.farmer');
    const modals = document.querySelectorAll('.modal');
    const closeButtons = document.querySelectorAll('.close-modal');

    farmers.forEach(farmer => {
        farmer.addEventListener('click', () => {
            const modalId = farmer.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            modal.style.display = 'flex';
        });
    });

    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            modals.forEach(modal => {
                modal.style.display = 'none';
            });
        });
    });

    window.addEventListener('click', (event) => {
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    });
}

window.addEventListener('scroll', handleScroll);
window.addEventListener('load', () => {
    handleScroll();
    handleModal();
});

function handleScroll() {
    const milestones = document.querySelectorAll('.milestone');
    const triggerPoint = window.innerHeight * 0.8;

    milestones.forEach((milestone) => {
        const milestoneTop = milestone.getBoundingClientRect().top;
        if (milestoneTop < triggerPoint) {
            milestone.classList.add('visible');
        }
    });
}

window.addEventListener('scroll', handleScroll);
window.addEventListener('load', handleScroll);