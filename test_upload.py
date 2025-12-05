from main import upload_csv
import os

# Ensure the file exists
if not os.path.exists("small_test.csv"):
    print("Creating dummy small_test.csv...")
    with open("small_test.csv", "w") as f:
        f.write("transferId,payerId,payeeId,amount,currency,scenario\n")
        f.write("1,27710000001,27710000002,100,USD,SUCCESS\n")

print("Testing upload of small_test.csv...")
result = upload_csv("small_test.csv")
print(result)
