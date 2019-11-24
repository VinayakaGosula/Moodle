import pickle
import os
import csv


def gen_csv(grades , columns , wut, team, path):	#vinayaka
	if team is 1 and wut is 1:
		final = path
		with open(final, 'w') as file:
			writer = csv.writer(file)
			row = ['Name']
			row.append('Team Name')
			row = row + columns
			row.append('comments')
			writer.writerow(row)
			for filename in os.listdir(grades):
				path = os.path.join(grades,filename)
				base=os.path.basename(path)
				name = os.path.splitext(base)[0]
				cur  = open(path,'rb')
				marks = pickle.load(cur)
				cur.close()
				ans = []
				ans.append(name)
				ans.append(marks[0][0])
				comments = ""
				for x in columns:
					cur_marks = 0
					total_marks = 0
					comments = comments + x
					comments = comments + "-"
					hmm = ""
					for y in marks:
						if(y[1].startswith(x)):
							cur_marks = cur_marks + y[2]
							total_marks = total_marks + y[3]
							hmm = hmm + y[4]
							hmm = hmm + ";"
					comments = comments + hmm
					comments = comments + "|"
					wtf = ""
					wtf = wtf + str(cur_marks)
					wtf = wtf + "/"
					wtf = wtf + str(total_marks)
					ans.append(wtf)
				ans.append(comments)
				writer.writerow(ans)
	elif team is 1 and wut is 0:
		final = path
		with open(final,'w') as file:
			writer = csv.writer(file)
			row = ['Team Name']
			row = row + columns
			row.append('comments')
			writer.writerow(row)
			for filename in os.listdir(grades):
				path = os.path.join(grades,filename)
				base = os.path.basename(path)
				name = os.path.splitext(base)[0]
				cur = open(path,'rb')
				marks = pickle.load(cur)
				cur.close()
				ans = []
				ans.append(marks[0][0])
				comments = ""
				for x in columns:
					cur_marks = 0
					total_marks = 0
					comments = comments + x
					comments = comments + "-"
					hmm = ""
					for y in marks:
						if(y[1].startswith(x)):
							cur_marks = cur_marks + y[2]
							total_marks = total_marks + y[3]
							hmm = hmm + y[4]
							hmm = hmm + ";"
					comments = comments + hmm
					comments = comments + "|"
					wtf = ""
					wtf = wtf + str(cur_marks)
					wtf = wtf + "/"
					wtf = wtf + str(total_marks)
					ans.append(wtf)
				ans.append(comments)
				writer.writerow(ans)
	else:
		final = path
		with open(final,'w') as file:
			writer = csv.writer(file)
			row = ['Name']
			row = row + columns
			row.append('comments')
			writer.writerow(row)
			for filename in os.listdir(grades):
				path = os.path.join(grades,filename)
				base=os.path.basename(path)
				name = os.path.splitext(base)[0]
				cur  = open(path,'rb')
				marks = pickle.load(cur)
				cur.close()
				ans = []
				ans.append(name)
				comments = ""
				for x in columns:
					cur_marks = 0
					total_marks = 0
					comments = comments + x
					comments = comments + "-"
					hmm = ""
					for y in marks:
						if(y[1].startswith(x)):
							cur_marks = cur_marks + y[2]
							total_marks = total_marks + y[3]
							hmm = hmm + y[4]
							hmm = hmm + ";"
					comments = comments + hmm
					comments = comments + "|"
					wtf = ""
					wtf = wtf + str(cur_marks)
					wtf = wtf + "/"
					wtf = wtf + str(total_marks)
					ans.append(wtf)
				ans.append(comments)
				writer.writerow(ans)
