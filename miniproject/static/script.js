$(document).ready(function () {
    // 모달 제출 이벤트
    $('#blogForm').submit(function (e) {
        e.preventDefault(); // 기본 제출 동작 방지
  
        // 입력된 이름과 주소 가져오기
        let blogName = $('#blogName').val();
        let blogAddress = $('#blogAddress').val();
  
        // 카드를 생성하고 속성 설정
        let card = document.createElement("div");
        card.className = "card";
        card.style.backgroundColor = "#333"; // 배경색을 어두운 톤으로 설정
  
        let cardBody = document.createElement("div");
        cardBody.className = "card-body";
  
        let cardTitle = document.createElement("h5");
        cardTitle.className = "card-title";
        cardTitle.innerText = "이름: " + blogName; // 이름 설정
  
        let cardText = document.createElement("p");
        cardText.className = "card-text";
        cardText.innerText = "주소: " + blogAddress; // 주소 설정
  
        cardBody.appendChild(cardTitle);
        cardBody.appendChild(cardText);
        card.appendChild(cardBody);
  
        // 카드를 카드 컨테이너에 추가
        let blogAddresses = document.getElementById("blogAddresses");
        blogAddresses.appendChild(card);
  
        // 모달 닫기
        $('#blogModal').modal('hide');
  
        // 입력 필드 지우기
        $('#blogName').val('');
        $('#blogAddress').val('');
    });
  });
  
  // 캘린더 초기화
  function initCalendar() {
    const calendarEl = document.getElementById("calendar");
  
    // 일정추가하면 카드처럼 등록하게 하고싶었으나 실패
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth", // 달력 초기 뷰 설정
        events: [
            {
                title: "예시1",
                start: "2023-10-15",
                end: "2023-10-17",
                backgroundColor: "#FF5733", // 이벤트의 배경색 설정
                borderColor: "#D64D00", // 이벤트의 테두리 색 설정
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
  
  // 호출하여 달력 초기화
  initCalendar();