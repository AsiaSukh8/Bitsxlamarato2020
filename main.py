import matplotlib.pyplot as plt
import numpy as np

def check_for_symptoms (patients, symptoms, plot, sex, status):
	symptoms_data = []
	figure_count = 1
	for symptom in symptoms.split(','):
		patient_with_symptom = 0
		patient_without_symptom = 0
		patient_undetermined = 0
		positive_males = 0
		positive_females = 0
		negative_males = 0
		negative_females = 0
		undetermined_males = 0
		undetermined_females = 0
		for patient in patients:
			if patient.split(',')[int(symptoms_general[1][symptoms_general[0].index(symptom)])] == symptoms_general[2][symptoms_general[0].index(symptom)]:
				patient_with_symptom += 1
				if patient.split(',')[2] == '1':
					positive_males += 1
				elif patient.split(',')[2] == '2':
					positive_females += 1
			elif patient.split(',')[int(symptoms_general[1][symptoms_general[0].index(symptom)])] == symptoms_general[3][symptoms_general[0].index(symptom)]:
				patient_without_symptom += 1
				if patient.split(',')[2] == '1':
					negative_males += 1
				elif patient.split(',')[2] == '2':
					negative_females += 1
			else:
				patient_undetermined += 1
				if patient.split(',')[2] == '1':
					undetermined_males += 1
				elif patient.split(',')[2] == '2':
					undetermined_females += 1
		data = [symptom, patient_with_symptom, patient_without_symptom, patient_undetermined, positive_males, positive_females, negative_males, negative_females, undetermined_males, undetermined_females]
		symptoms_data.append(data)
		if plot:
			plt.figure(figure_count)
			plot_data = []
			colors = []
			legend = []
			if not sex:
				plot_data = [patient_with_symptom, patient_without_symptom, patient_undetermined]
				colors = ['#e0f8f5', '#f8b195', '#a8adb4']
				legend = ["Positive (" + str(round(patient_with_symptom/(patient_with_symptom+patient_without_symptom+patient_undetermined)*100, 2)) + "%)", "Negative (" + str(round(patient_without_symptom/(patient_with_symptom+patient_without_symptom+patient_undetermined)*100, 2)) + "%)", "Undetermined (" + str(round(patient_undetermined/(patient_with_symptom+patient_without_symptom+patient_undetermined)*100, 2)) + "%)"]
			else:
				plot_data = [positive_males, positive_females, patient_with_symptom-positive_males-positive_females, negative_males, negative_females, patient_without_symptom-negative_males-negative_females, undetermined_males, undetermined_females, patient_undetermined-undetermined_males-undetermined_females]
				colors = ['#e0f8f5', '#beede5', '#a7d9c9', '#f8b195', '#ffbd77', '#ffa13e', '#a8adb4', '#c3c8cd', '#d2d6d9']
				legend = ["Positive Male (" + str(round(positive_males/(patient_with_symptom+patient_without_symptom+patient_undetermined)*100, 2)) + "%)", "Positive Female (" + str(round(positive_females/(patient_with_symptom+patient_without_symptom+patient_undetermined)*100, 2)) + "%)", "Positive Undetermined (" + str(round((patient_with_symptom-positive_males-positive_females)/(patient_with_symptom+patient_without_symptom+patient_undetermined)*100, 2)) + "%)", "Negative Male (" + str(round(negative_males/(patient_with_symptom+patient_without_symptom+patient_undetermined)*100, 2)) + "%)", "Negative Female (" + str(round(negative_females/(patient_with_symptom+patient_without_symptom+patient_undetermined)*100, 2)) + "%)", "Negative Undetermined (" + str(round((patient_without_symptom-negative_males-negative_females)/(patient_with_symptom+patient_without_symptom+patient_undetermined)*100, 2)) + "%)", "Undetermined Male (" + str(round(undetermined_males/(patient_with_symptom+patient_without_symptom+patient_undetermined)*100, 2)) + "%)", "Undetermined Female (" + str(round(undetermined_females/(patient_with_symptom+patient_without_symptom+patient_undetermined)*100, 2)) + "%)", "Undetermined Undetermined (" + str(round((patient_undetermined-undetermined_males-undetermined_females)/(patient_with_symptom+patient_without_symptom+patient_undetermined)*100, 2)) + "%)"]
			plt.pie (plot_data, colors=colors)
			plt.title (symptom + "(" + status + ")")
			plt.legend(legend, loc='lower left', bbox_to_anchor=(-.1, 0), fontsize='x-small')
			plt.tight_layout(h_pad=1)
			figure_count += 1
	if plot:
		plt.show()
	return symptoms_data


def compare(ppd, npd, plot, min_difference, sex):
	normalized_ppd = []
	normalized_npd = []
	conditions = []
	positive_ppd = []
	positive_npd = []
	negative_ppd = []
	negative_npd = []
	positive_ppd_males = []
	positive_ppd_females = []
	positive_ppd_undetermined = []
	positive_npd_males = []
	positive_npd_females = []
	positive_npd_undetermined = []
	for value in ppd:
		normalized_ppd.append([value[0], value[1]/(value[1]+value[2]), value[2]/(value[1]+value[2]), value[3]])
		conditions.append(value[0])
		positive_ppd.append(value[1]/(value[1]+value[2]))
		negative_ppd.append(value[2]/(value[1]+value[2]))
		if sex:
			positive_ppd_males.append(value[4]/(value[1]+value[2]))
			positive_ppd_females.append(value[5]/(value[1]+value[2]))
			positive_ppd_undetermined.append((value[1]-value[4]-value[5])/(value[1]+value[2]))
	for value in npd:
		normalized_npd.append([value[0], value[1]/(value[1]+value[2]), value[2]/(value[1]+value[2]), value[3]])
		positive_npd.append(value[1]/(value[1]+value[2]))
		negative_npd.append(value[2]/(value[1]+value[2]))
		if sex:
			positive_npd_males.append(value[4]/(value[1]+value[2]))
			positive_npd_females.append(value[5]/(value[1]+value[2]))
			positive_npd_undetermined.append((value[1]-value[4]-value[5])/(value[1]+value[2]))
	differences = []
	for i in range (len(positive_ppd)):
		differences.append(positive_ppd[i]-positive_npd[i])

	weighted_conditions = []
	for i in range (len(differences)):
		if (positive_ppd[i]+positive_npd[i]) > 0:
			differences[i] = differences[i]/(positive_ppd[i] + positive_npd[i])
		else:
			differences[i] = 0
		if abs(differences[i]) >= min_difference/100:
			weighted_conditions.append([conditions[i], differences[i]])
#			print (conditions[i] + " has a difference of " + str(differences[i]))
	if plot:
		fig,ax = plt.subplots(2)
		x = np.arange(len(conditions))
		plt.title("Relation between Covid and non covid symptomatology")
		ax[0].set_title("COVID Results")
		if not sex:
			ax[0].bar(x, positive_ppd, width=0.35)
		if sex:
			bar_males = ax[0].bar(x, positive_ppd_males, width=0.35)
			bar_females = ax[0].bar(x, positive_ppd_females, width=0.35, bottom=positive_ppd_males)
			bar_undetermined = ax[0].bar(x, positive_ppd_undetermined, width=0.35, bottom=positive_ppd_females)
		ax[0].bar(x+0.35, negative_ppd, width=0.35)
		ax[0].set_ylim([0,1])
		ax[1].set_title("NON-COVID Results")
		legend = []
		if not sex:
			ax[1].bar(x, positive_npd, width=0.35)
			legend.append ("Positive")
		if sex:
			bar_males = ax[1].bar(x, positive_npd_males, width=0.35)
			legend.append ("Male")
			bar_females = ax[1].bar(x, positive_npd_females, width=0.35, bottom=positive_npd_males)
			legend.append("Female")
			bar_undetermined = ax[1].bar(x, positive_npd_undetermined, width=0.35, bottom=positive_npd_females)
			legend.append("Undetermined")
		ax[1].bar(x+0.35, negative_npd, width=0.35)
		legend.append("Negative")
		ax[1].set_ylim([0,1])

		plt.setp(ax[1], xticks=x, xticklabels=conditions)
		plt.setp(ax[1].get_xticklabels(), rotation=90)
		plt.setp(ax[0], xticks=x, xticklabels=conditions)
		plt.legend(legend, loc='upper right', fontsize='x-small')

		for a in fig.get_axes():
			a.label_outer()
#		fig.tight_layout()

		fig2,ax2 = plt.subplots()
		x = np.arange(len(differences))
		y = np.ones(len(differences))
		y2 = np.ones(len(differences))
		plt.title("Difference between COVID and non-COVID symptoms")
		plt.stem (x, differences, use_line_collection=True)
		plt.plot (x, np.ones(len(x))*min_difference/100, 'r--', linewidth=0.5)
		plt.plot (x, np.ones(len(x))*min_difference/100*-1, 'r--', linewidth=0.5)
		plt.xticks(np.arange(len(differences)), conditions, rotation=90)
#		fig2.tight_layout()
		plt.show()
	return weighted_conditions


def check_for_multiple_symptoms (patients_positive, patients_negative, symptoms_raw, plot, gender):
	symptoms = symptoms_raw.split(',')
	symptoms_values = []
	result_positive = [0, 0, 0]
	for symptom in symptoms:
		symptoms_values.append(int(symptoms_general[1][symptoms_general[0].index(symptom)]))
	for patient in patients_positive:
		if patient.split(',')[2] == gender:
			has_symptoms = True
			is_undetermined = False
			for i in symptoms_values:
				if patient.split(',')[i] == symptoms_general[3][symptoms_general[0].index(symptoms[symptoms_values.index(i)])]:
					has_symptoms = False
				elif not patient.split(',')[i] == symptoms_general[2][symptoms_general[0].index(symptoms[symptoms_values.index(i)])] and not patient.split(',')[i] == symptoms_general[3][symptoms_general[0].index(symptoms[symptoms_values.index(i)])]:
					is_undetermined = True
			if has_symptoms and not is_undetermined:
				result_positive[0] += 1
			elif not has_symptoms and not is_undetermined:
				result_positive[1] += 1
			else:
				result_positive[2] += 1
	result_negative = [0, 0, 0]
	for patient in patients_negative:
		if patient.split(',')[2] == gender:
			has_symptoms = True
			is_undetermined = False
			for i in symptoms_values:
				if patient.split(',')[i] == symptoms_general[3][symptoms_general[0].index(symptoms[symptoms_values.index(i)])]:
					has_symptoms = False
				elif not patient.split(',')[i] == symptoms_general[2][symptoms_general[0].index(symptoms[symptoms_values.index(i)])] and not patient.split(',')[i] == symptoms_general[3][symptoms_general[0].index(symptoms[symptoms_values.index(i)])]:
					is_undetermined = True
			if has_symptoms and not is_undetermined:
				result_negative[0] += 1
			elif not has_symptoms and not is_undetermined:
				result_negative[1] += 1
			else:
				result_negative[2] += 1
	if plot:
		if (result_positive[0]+result_positive[1]+result_positive[2]) > 0:
			plt.figure(1)
			plt.title ("Presence of simultaneous " + symptoms_raw + " (Positive " + genders[1][genders[0].index(gender)] + ")")
			colors = ['#e0f8f5', '#f8b195', '#a8adb4']
			plt.pie(result_positive, startangle=90, colors=colors)
			plt.legend (["Presence (" + str(round(100*result_positive[0]/(result_positive[0]+result_positive[1]+result_positive[2]), 2)) + "%)", "Absence (" + str(round(100*result_positive[1]/(result_positive[0]+result_positive[1]+result_positive[2]), 2)) + "%)", "Undetermined (" + str(round(100*result_positive[2]/(result_positive[0]+result_positive[1]+result_positive[2]), 2)) + "%)"], loc='lower left', bbox_to_anchor=(-0.1, 0), fontsize='x-small')
		if (result_negative[0]+result_negative[1]+result_negative[2]) > 0:
			plt.figure(2)
			plt.title ("Presence of simultaneous " + symptoms_raw + " (Negative " + genders[1][genders[0].index(gender)] + ")")
			plt.pie (result_negative, startangle=90, colors=colors)
			plt.legend (["Presence (" + str(round(100*result_negative[0]/(result_negative[0]+result_negative[1]+result_negative[2]), 2)) + "%)", "Absence (" + str(round(100*result_negative[1]/(result_negative[0]+result_negative[1]+result_negative[2]), 2)) + "%)", "Undetermined (" + str(round(result_negative[2]*100/(result_negative[0]+result_negative[1]+result_negative[2]),2)) + "%)"], loc='lower left', bbox_to_anchor=(-0.1, 0), fontsize='x-small')
		plt.show()
	return result_positive, result_negative


def generate_possible_combinations (conditions):
	positive_conditions = []
	negative_conditions = []
	combinations = []
	for condition in conditions:
		if condition[1] > 0:
			positive_conditions.append(condition[0])
		if condition[1] < 0:
			negative_conditions.append(condition[0])
	for i in range(len(positive_conditions)):
		for j in range(i+1, (len(positive_conditions))):
			combinations.append([positive_conditions[i]+','+positive_conditions[j], 'c'])
	for i in range(len(negative_conditions)):
		for j in range(i+1, (len(negative_conditions))):
			combinations.append([negative_conditions[i]+','+negative_conditions[j], 'o'])
	return combinations


f = open ("./Files/COPEDICATClinicSympt_DATA_2020-12-17_1642.csv", 'r')

data = []
for line in f:
	data.append(line)

f.close()

patients_COVID_Positive = []
patients_COVID_Negative = []

for value in data:
	if value.split(',')[31] == '1' and (value.split(',')[117] == '1' or value.split(',')[122] == '1' or value.split(',')[107] == '1'):
		patients_COVID_Positive.append(value)
	elif value.split(',')[31] == '1' and ((value.split(',')[117] == '2' or value.split(',')[117] == '') and (value.split(',')[122] == '2' or value.split(',')[122] == '') and (value.split(',')[107] == '2' or value.split(',')[107] == '')):
		patients_COVID_Negative.append(value)

symptoms_general = [["Fever", "Cough", "Dysphonia", "Dyspnea", "Tachypnea", "Alterated Respiratory Auscultation",
		     "Odynophagia", "Nasal Congestion", "Fatigue", "Headache", "Conjuntivitis", "Retro-ocular Pain",
		     "Gastrointestinal Symptoms", "Skin Signs", "Lymphadenopathy", "Hepatomegaly", "Splenomegaly",
		     "Hemorrhagies", "Irritability", "Neurologic Manifestations", "Shock", "Taste Alteration",
		     "Smell Alteration"],
		    ["33", "38", "42", "44", "46", "48", "52", "54", "56", "58", "60", "62", "64", "69", "74", "76",
		     "78", "80", "82", "84", "91", "93", "95"],
		    ['1', '1', '1', '1', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
		     '1', '1', '1', '1'],
		    ['2', '2', '2', '2', '2', '1', '2', '2', '2', '2', '2', '2', '0', '0', '2', '2', '2', '2', '2',
		     '0', '0', '0', '0']]
genders = [['1', '2', '3'],["Male", "Female", "Undetermined"]]

#positive_patients_data = check_for_symptoms(patients_COVID_Positive, "Fever,Cough,Dysphonia,Dyspnea,Tachypnea,Alterated Respiratory Auscultation,Odynophagia,Nasal Congestion,Fatigue,Headache,Conjuntivitis,Retro-ocular Pain,Gastrointestinal Symptoms,Skin Signs,Lymphadenopathy,Hepatomegaly,Splenomegaly,Hemorrhagies,Irritability,Neurologic Manifestations,Shock,Taste Alteration,Smell Alteration", False, True, 'Positive')
#negative_patients_data = check_for_symptoms(patients_COVID_Negative, "Fever,Cough,Dysphonia,Dyspnea,Tachypnea,Alterated Respiratory Auscultation,Odynophagia,Nasal Congestion,Fatigue,Headache,Conjuntivitis,Retro-ocular Pain,Gastrointestinal Symptoms,Skin Signs,Lymphadenopathy,Hepatomegaly,Splenomegaly,Hemorrhagies,Irritability,Neurologic Manifestations,Shock,Taste Alteration,Smell Alteration", False, True, 'Negative')
positive_patients_data = check_for_symptoms(patients_COVID_Positive, "Fever,Smell Alteration,Dyspnea,Skin Signs", False, True, 'Positive')
negative_patients_data = check_for_symptoms(patients_COVID_Negative, "Fever,Smell Alteration,Dyspnea,Skin Signs", False, True, 'Negative')
weighted_conditions = compare (positive_patients_data, negative_patients_data, True, 0, True)
combinations = generate_possible_combinations(weighted_conditions)
probabilities = []
for gender in genders[0]:
	for combination in combinations:
		mult_positive_patients_data,mult_negative_patients_data = check_for_multiple_symptoms (patients_COVID_Positive, patients_COVID_Negative, combination[0], True, gender)
		if combination[1] == 'c':
			if not ((mult_positive_patients_data[0]+mult_positive_patients_data[1]) == 0 or (mult_negative_patients_data[0]+mult_negative_patients_data[1]) == 0) and not mult_negative_patients_data[0] == 0:
				x = (mult_positive_patients_data[0]/(mult_positive_patients_data[0]+mult_positive_patients_data[1]))/(mult_negative_patients_data[0]/(mult_negative_patients_data[0]+mult_negative_patients_data[1]))
				probabilities.append([combination[0], x/(x+1), gender])
#				print (combination[0] + ': ' + str(x/(x+1)))
			else:
				if mult_negative_patients_data[0] == 0 and not (mult_negative_patients_data[0]+mult_negative_patients_data[1]) == 0:
					probabilities.append([combination[0], 1, gender])
#					print (combination[0] + ': 1')
				if mult_negative_patients_data[0] == 0 and (mult_positive_patients_data[0]+mult_negative_patients_data[1]) == 0:
					probabilities.append([combination[0], 'Cannot be computed', gender])
#					print (combination[0] + ': Cannot be computed')
		if combination[1] == 'o':
			if not ((mult_positive_patients_data[0]+mult_positive_patients_data[1]) == 0 or (mult_negative_patients_data[0]+mult_negative_patients_data[1]) == 0) and not mult_positive_patients_data[0] == 0:
				x = (mult_negative_patients_data[0]/(mult_negative_patients_data[0]+mult_negative_patients_data[1]))/(mult_positive_patients_data[0]/(mult_positive_patients_data[0]+mult_positive_patients_data[1]))
				probabilities.append([combination[0], 1-(x/(x+1)), gender])
#				print (combination[0] + ': ' + str(1-(x/(x+1))))
			else:
				if mult_positive_patients_data[0] == 0 and not (mult_positive_patients_data[0]+mult_positive_patients_data[1]) == 0:
					probabilities.append([combination[0], 0, gender])
#					print (combination[0] + ': 0')
				if mult_negative_patients_data[0] == 0 and (mult_positive_patients_data[0]+mult_positive_patients_data[1]) == 0:
					probabilities.append([combination[0], 'Cannot be computed', gender])
#					print (combination[0] + ': Cannot be computed')
f = open ('./Output/Probabilities.txt', 'w+')
for probability in probabilities:
	f.write(probability[0] + ' (' + str(genders[1][int(genders[0].index(probability[2]))]) + '): ' + str(probability[1]) + '\n')
f.close()
