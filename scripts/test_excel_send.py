from app.excel_service import read_targets_from_excel, write_results_to_excel
from app.sender import send_many


def main():
    file_path = "sample.xlsx"

    rows = read_targets_from_excel(file_path)
    print(f"읽은 행 수: {len(rows)}")

    results = send_many(rows)
    write_results_to_excel(file_path, results)

    print("발송 결과:")
    for item in results:
        print(item)


if __name__ == "__main__":
    main()