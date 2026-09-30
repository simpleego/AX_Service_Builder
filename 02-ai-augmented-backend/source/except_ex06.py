# process_scores.py
students = ["김철수", "이영희", "박민수", "최유진"]

for student in students:
    try:
        with open(f"{student}_성적.txt", 'r') as f:
            score = f.read()
            print(f"{student}의 성적: {score}")
    except FileNotFoundError:
        print(f"{student}의 성적 파일이 없습니다. 건너뜁니다.")
        continue  # 다음 학생으로 넘어감
