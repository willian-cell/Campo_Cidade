function login(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Verifica se o login e senha estão corretos
    if (email === 'adm@campocidade' && password === '123456789') {
        document.getElementById('loginPage').style.display = 'none';
        document.getElementById('dashboard').style.display = 'block';
    } else {
        alert('Usuário ou senha inválidos!');
    }
}


function logout() {
    document.getElementById('dashboard').style.display = 'none';
    document.getElementById('loginPage').style.display = 'flex';
}

function toggleDetails(button, plantDate) {
    const details = button.nextElementSibling;
    const harvestTimer = details.querySelector('.harvest-timer');
    if (details.style.display === 'block') {
        details.style.display = 'none';
    } else {
        details.style.display = 'block';
        updateHarvestTimer(harvestTimer, plantDate);
    }
}

function updateHarvestTimer(element, plantDate) {
    const plantDateObj = new Date(plantDate);
    const harvestDateObj = new Date(plantDateObj);
    harvestDateObj.setDate(plantDateObj.getDate() + 35);

    const today = new Date();
    const diffTime = harvestDateObj - today;

    if (diffTime > 0) {
        const daysLeft = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        element.textContent = `${daysLeft} dias restantes`;
    } else {
        element.textContent = `Pronto para colheita!`;
    }
}

function redirectToDetails(type) {
    document.getElementById('dashboard').style.display = 'none';
    document.getElementById('detailsPage').style.display = 'block';
    initializeCharts();
}

function initializeCharts() {
    new Chart(document.getElementById('growthChart'), {
        type: 'line',
        data: {
            labels: ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4'],
            datasets: [{ label: 'Crescimento das Plantas', data: [5, 10, 20, 35], borderColor: 'green' }]
        }
    });
    // Adicione os outros gráficos aqui
}

function goBack() {
    document.getElementById('detailsPage').style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';
}
