# Quiz.py
import json
import os
import random

STATE_FILE = "state.json"  # 프로젝트 루트에 저장


class Quiz:
    """개별 퀴즈를 표현하는 클래스"""

    def __init__(self, question, choices, answer, hint=""):
        self.question = question      # 문제 (str)
        self.choices = choices        # 선택지 (list, 4개)
        self.answer = answer          # 정답 번호 (1~4)
        self.hint = hint              # 힌트 (보너스)

    def show(self):
        """문제와 선택지를 출력"""
        print(f"\n{self.question}")
        for i, choice in enumerate(self.choices, start=1):
            print(f"  {i}. {choice}")

    def is_correct(self, user_answer):
        """정답 여부 확인"""
        return self.answer == user_answer

    def to_dict(self):
        """JSON 저장용 딕셔너리 변환"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @staticmethod
    def from_dict(data):
        """딕셔너리 -> Quiz 객체"""
        return Quiz(
            data["question"],
            data["choices"],
            data["answer"],
            data.get("hint", ""),
        )


def get_default_quizzes():
    """기본 퀴즈 데이터 (Python 기초 주제, 5개 이상)"""
    return [
        Quiz("변수를 선언할 때 사용하는 올바른 방식은?",
             ["int x = 5", "x = 5", "var x = 5", "x := 5"], 2,
             "Python은 타입을 명시하지 않아요."),
        Quiz("다음 중 리스트(list)를 만드는 문법은?",
             ["{1, 2, 3}", "(1, 2, 3)", "[1, 2, 3]", "<1, 2, 3>"], 3,
             "대괄호를 사용해요."),
        Quiz("문자열 타입을 나타내는 것은?",
             ["int", "str", "bool", "float"], 2,
             "string의 약자예요."),
        Quiz("True/False 값을 가지는 자료형은?",
             ["int", "list", "bool", "dict"], 3,
             "참/거짓을 표현해요."),
        Quiz("반복 횟수가 정해졌을 때 주로 쓰는 반복문은?",
             ["while", "for", "if", "def"], 2,
             "범위를 돌 때 자주 써요."),
        Quiz("함수를 정의할 때 사용하는 키워드는?",
             ["func", "function", "def", "lambda"], 3,
             "3글자 키워드예요."),
    ]


class QuizGame:
    """게임 전체를 관리하는 클래스"""

    def __init__(self):
        self.quizzes = []       # Quiz 객체 목록
        self.best_score = 0     # 최고 점수
        self.played = False     # 플레이 여부
        self.load()

    # ---------- 파일 입출력 ----------
    def load(self):
        """state.json 불러오기 (없거나 손상 시 기본 데이터)"""
        if not os.path.exists(STATE_FILE):
            self.quizzes = get_default_quizzes()
            self.best_score = 0
            return
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data["quizzes"]]
            self.best_score = data.get("best_score", 0)
            if not self.quizzes:
                self.quizzes = get_default_quizzes()
        except (json.JSONDecodeError, KeyError, OSError):
            print("⚠ 데이터 파일이 손상되어 기본 데이터로 복구합니다.")
            self.quizzes = get_default_quizzes()
            self.best_score = 0

    def save(self):
        """state.json에 저장 (UTF-8)"""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            print("⚠ 파일 저장 중 오류가 발생했습니다.")

    # ---------- 공통 입력 처리 ----------
    def input_number(self, prompt, min_val, max_val):
        """숫자 입력 + 예외 처리 (재입력 흐름)"""
        while True:
            raw = input(prompt).strip()
            if raw == "":
                print("입력이 비어 있습니다. 다시 입력하세요.")
                continue
            if not raw.lstrip("-").isdigit():
                print("숫자만 입력할 수 있습니다. 다시 입력하세요.")
                continue
            num = int(raw)
            if num < min_val or num > max_val:
                print(f"{min_val}~{max_val} 범위의 숫자를 입력하세요.")
                continue
            return num

    def input_text(self, prompt):
        """빈 문자열 방지 입력"""
        while True:
            raw = input(prompt).strip()
            if raw == "":
                print("내용을 입력하세요.")
                continue
            return raw

    # ---------- 메뉴 ----------
    def show_menu(self):
        print("\n===== 파이썬 기초 퀴즈 게임 =====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 퀴즈 삭제")
        print("5. 점수 확인")
        print("6. 종료")

    # ---------- 기능들 ----------
    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        quizzes = self.quizzes[:]
        random.shuffle(quizzes)  # 보너스: 랜덤 출제
        score = 0
        for quiz in quizzes:
            quiz.show()
            ans = self.input_number("정답 번호를 입력하세요 (1~4): ", 1, 4)
            if quiz.is_correct(ans):
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")
        print(f"\n총 {len(quizzes)}문제 중 {score}개 맞혔습니다!")
        self.played = True
        if score > self.best_score:
            self.best_score = score
            print("🎉 최고 점수를 갱신했습니다!")
        self.save()

    def add_quiz(self):
        question = self.input_text("문제를 입력하세요: ")
        choices = []
        for i in range(1, 5):
            c = self.input_text(f"선택지 {i}: ")
            choices.append(c)
        answer = self.input_number("정답 번호 (1~4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        self.save()
        print("✅ 퀴즈가 추가되었습니다.")

    def list_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        print(f"\n총 {len(self.quizzes)}개의 퀴즈가 있습니다.")
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"{i}. {quiz.question}")

    def delete_quiz(self):
        """등록된 퀴즈를 선택해 삭제하고 파일에 반영"""
        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        # ① 목록 보여주기 (어떤 퀴즈를 지울지 선택)
        print(f"\n총 {len(self.quizzes)}개의 퀴즈가 있습니다.")
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"{i}. {quiz.question}")
        print("0. 취소")

        # ② 삭제할 번호 입력 (0=취소 가능)
        num = self.input_number(
            f"삭제할 퀴즈 번호 (1~{len(self.quizzes)}, 0=취소): ",
            0, len(self.quizzes))
        if num == 0:
            print("삭제를 취소했습니다.")
            return

        # ③ 삭제 전 재확인 (실수 방지)
        target = self.quizzes[num - 1]
        print(f"[{num}번] {target.question}")
        confirm = self.input_number(
            "정말 삭제하시겠습니까? (1=예, 0=아니오): ", 0, 1)
        if confirm == 0:
            print("삭제를 취소했습니다.")
            return

        # ④ 실제 삭제 (화면번호 num -> 리스트 인덱스 num-1)
        removed = self.quizzes.pop(num - 1)

        # ⑤ 파일에 반영
        self.save()
        print(f"🗑 '{removed.question}' 퀴즈가 삭제되었습니다.")

    def show_score(self):
        if not self.played:
            print("아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"현재 최고 점수: {self.best_score}점")

    # ---------- 메인 루프 ----------
    def run(self):
        while True:
            try:
                self.show_menu()
                choice = self.input_number("메뉴 선택 (1~6): ", 1, 6)
                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.delete_quiz()
                elif choice == 5:
                    self.show_score()
                elif choice == 6:
                    print("프로그램을 종료합니다. 안녕히 가세요!")
                    self.save()
                    break
            except (KeyboardInterrupt, EOFError):
                print("\n입력이 중단되어 안전하게 종료합니다.")
                self.save()
                break


if __name__ == "__main__":
    game = QuizGame()
    game.run()
