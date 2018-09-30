

from file_read_backwards import FileReadBackwards

with FileReadBackwards('wfo-saas-webapp-promote-prod-admin_198_final.txt', encoding='utf-8') as frb:
        while True:
            line = frb.readline().rstrip('\n')
            print(line)
            if line == "Finished: SUCCESS":
                print("Success is done ! breaking")
                break
            else:
                print("working")

