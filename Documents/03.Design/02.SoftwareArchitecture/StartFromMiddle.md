# Start From Middle

이미 반죽이 되어버린 상황에서 시작하려면, 먼저 얽혀있는 책임의 분리부터 시작해야 한다. 아직 각 컴포넌틔의 책임을 명확하게 하지 않았기에 시스템의 모든 부분이 다 똑같아 보일 것이다. 이를 고치려면 책임을 분리하고 명확한 바운더리를 설정하는 것에서 부터 시작해야 한다.

## 서비스 레이어를 만드는 것부터 시작하자.

시스템의 유즈케이스에서 시작하자. 유저 인터페이스가 있다면 어떤 액션을 수행하는가? 백엔드 처리 컴포넌트가 있다면 각각의 cron job 또는 celery job은 하나의 유즈케이스이다. 각 유즈케이스는 명령형 이름을 갖을 필요가 있다. 

이런 각각의 유즈케이스를 위해 일을 될 수 있도록 조정하고 처리하는 지원하는 행위들을 하나의 펑션이나 클래스로 생성하는 것이 목표이며 다음을 따른다.

- 필요하다면 데이타베이스 트랜잭션을 시작한다.
- 필요한 데이터를 Fetch한다.
- 사전 조건을 체크한다.
- 도메인 모델을 업데이트 한다.
- 변화를 영속화 한다.

각각의 유즈케이스는 원자적 단위로 성공하거나 실패한다. 하나의 유즈케이스를 다른 곳에어 호출 할지도 모른다. 다 좋다. 그리고 데이터베이스 트랜젹신이 길게 가는것은 피하자

이는 도메인 모델에서 조정 또는 데이터 억세스 코드를 유즈 케이스로 끄집어내는 좋은 기회이다. 또, 도메인 모델에서 I/O 관심사도 유즈케이스로 끄집어 낸다. 

이를 통해서 프로그램이 정확히 무엇을 하는지 또 오퍼레이션의 시작과 끝을 명확하게 할 수 있다. 이는 또한 순수한 도메인 모델로 나아가게 된다.

[*Working Effectively with Legacy Code* by Michael C. Feathers (Prentice Hall)](https://book.naver.com/bookdb/book_detail.nhn?bid=14032002)

## 어그리게이트와 바운디드 컨텍스트 식별

각 유즈케이스는 한번에 하나의 어그리게이트만 업데이트 해야 한다.

핸들러는 하나의 어그리게이트를 레포지토리에서 페치해서 상태를 수정하고 결과로서 발생한 이벤테를 일으킨다.

만약 시스템의 다른 부분에서 데이터가 필요하다면 실제 모델을 사용하는것은 괜찮지만, 한 트랜잭션에서 여러 어그리게이트를 업데이트 하는 일은 피해야 한다. 코드를 여러개의 어그리게이트로 분리하기로 결정했다면 명시적으로 결과적으로 일관성을 유지하도록 만들어야 한다.

대부분 클래스의 직접 참조를 식별자로 대체하면 된다.

양방향 관계는 어그리게이트가 옳지 않다는 신호이다.
