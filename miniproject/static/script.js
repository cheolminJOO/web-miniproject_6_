$(document).ready(function () {
    initializeBlogForm();
    initCalendar();
});

function initializeBlogForm() {
    $('#blogForm').submit(function (e) {
        e.preventDefault();

        let blogName = $('#blogName').val();
        let blogAddress = $('#blogAddress').val();

        if(blogName && blogAddress) {
            createBlogCard(blogName, blogAddress);
            clearBlogForm();
        } else {
            alert("이름과 주소를 모두 입력해주세요.");
        }
    });
}

function createBlogCard(name, address) {
    // 카드 생성
    let card = document.createElement("div");
    card.className = "card";
    card.addEventListener('click', function() {
        window.open(address, '_blank');
    });
    card.style.cursor = "pointer";  // 마우스 커서를 손가락 모양으로 변경

    let cardBody = document.createElement("div");
    cardBody.className = "card-body";

    let cardTitle = document.createElement("h5");
    cardTitle.className = "card-title";
    cardTitle.innerText = name;

    let cardText = document.createElement("p");
    cardText.className = "card-text";
    cardText.innerText = "주소: " + address;

    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardText);
    card.appendChild(cardBody);

    let blogAddresses = document.getElementById("blogAddresses");
    blogAddresses.appendChild(card);
    // http:// 또는 https://로 시작하는지 확인
    if (!address.startsWith('http://') && !address.startsWith('https://')) {
        address = 'http://' + address;
    }
}

function clearBlogForm() {
    $('#blogName').val('');
    $('#blogAddress').val('');
    $('#blogModal').modal('hide');
}

function initCalendar() {
    const calendarEl = document.getElementById("calendar");

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        events: [
            {
                title: "예시1",
                start: "2023-10-15",
                end: "2023-10-17",
                backgroundColor: "#FF5733",
                borderColor: "#D64D00",
            },
            {
                title: "예시2",
                start: "2023-10-20",
                backgroundColor: "#007bff",
                borderColor: "#007bff",
            },
        ],
    });

    calendar.render();
}