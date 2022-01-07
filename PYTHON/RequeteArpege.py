import datetime
import time
import requests
import os
import os.path
import sys

class ProblemeMeteoFrance(Exception):
	pass

def DateDuPlusRecentRun():
	InstantPresent=datetime.datetime.utcnow()
	# InstantChoisi est la meme date que InstantPrecedent, avec simplement le nombre d'heure-minute-seconde mis a zero
	InstantChoisi=datetime.datetime( InstantPresent.year, InstantPresent.month, InstantPresent.day, InstantPresent.hour, 0, 0, 0)
	# ON CONSIDERE QUE LE PLUS RECENT RUN DISPONIBLE EST CELUI LANCE AU MOINS 6H AVANT LA DATE ACTUELLE
#	InstantPrecedent = InstantChoisi - datetime.timedelta(hours=6)
	InstantPrecedent = InstantChoisi - datetime.timedelta(hours=3)

# LES RUNS ARPEGE ONT LIEU AUX ECHEANCES 0, 6, 12 ET 18H CHAQUE JOUR
	if (InstantPrecedent.hour>18):
		InstantRequete=datetime.datetime( InstantPrecedent.year, InstantPrecedent.month, InstantPrecedent.day, 18, 0, 0, 0)
	elif (InstantPrecedent.hour>12):
		InstantRequete=datetime.datetime( InstantPrecedent.year, InstantPrecedent.month, InstantPrecedent.day, 12, 0, 0, 0)
	elif (InstantPrecedent.hour>6):
		InstantRequete=datetime.datetime( InstantPrecedent.year, InstantPrecedent.month, InstantPrecedent.day, 6, 0, 0, 0)
	else:
		InstantRequete=datetime.datetime( InstantPrecedent.year, InstantPrecedent.month, InstantPrecedent.day, 0, 0, 0, 0)

	return InstantRequete

# FIN DE DateDuPlusRecentRun

def RequetePrevisionPourUnDeltaEnHeure( NomPackage, DeltaEnHeure):

	DateDuRun = DateDuPlusRecentRun();

	# INSTANT PRESENT
	InstantPresent=datetime.datetime.utcnow()
	# HEURE CORRESPONDANTE (ON MET LES MINUTES ET SECONDES A ZERO)
	InstantChoisi=datetime.datetime( InstantPresent.year, InstantPresent.month, InstantPresent.day, InstantPresent.hour, 0, 0, 0)

	# INTERVALLE ENTRE L HEURE ACTUELLE ET LE PLUS RECENT RUN DISPONIBLE
	IntervalleEntreLeRunEtLePresent = InstantChoisi - DateDuRun

	# ON RAJOUTE LE DeltaEnHeure SPECIFIE EN ARGUMENT
	IntervalleEntreLeRunEtLaPrevisionVoulue = IntervalleEntreLeRunEtLePresent + datetime.timedelta( hours=DeltaEnHeure)

	if (IntervalleEntreLeRunEtLaPrevisionVoulue <= datetime.timedelta(hours=24)):
		Fourchette = "00H24H"
	elif (IntervalleEntreLeRunEtLaPrevisionVoulue <= datetime.timedelta(hours=48)):
		Fourchette = "27H48H"
	elif (IntervalleEntreLeRunEtLaPrevisionVoulue <= datetime.timedelta(hours=72)):
		Fourchette = "51H72H"
	elif (IntervalleEntreLeRunEtLaPrevisionVoulue <= datetime.timedelta(hours=102)):
		Fourchette = "75H102H"
	elif (IntervalleEntreLeRunEtLaPrevisionVoulue <= datetime.timedelta(hours=114)):
		Fourchette = "103H114H"
	else:
		sys.stderr.write("prevision trop lointaine, on reduit a la fourchette 105H114H\n")
		Fourchette = "103H114H"

	Package =  NomPackage

# HP1,2 IP1,2,3,4 SP1,2
	monNouveauToken="eyJ4NXQiOiJOVGRtWmpNNFpEazNOalkwWXpjNU1tWm1PRGd3TVRFM01XWXdOREU1TVdSbFpEZzROemM0WkE9PSIsImtpZCI6ImdhdGV3YXlfY2VydGlmaWNhdGVfYWxpYXMiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJnZW9yZ2VzLXBpZXJyZS5ib25uZWF1QGNhcmJvbi5zdXBlciIsImFwcGxpY2F0aW9uIjp7Im93bmVyIjoiZ2Vvcmdlcy1waWVycmUuYm9ubmVhdSIsInRpZXJRdW90YVR5cGUiOm51bGwsInRpZXIiOiJVbmxpbWl0ZWQiLCJuYW1lIjoidmlzdWFsaXNhdGlvbklORk81IiwiaWQiOjE4NSwidXVpZCI6ImU0MmNmNmVkLWQ4N2EtNGFmYy1hYWI1LTkyN2JlNmNlZjE0ZCJ9LCJpc3MiOiJodHRwczpcL1wvcG9ydGFpbC1hcGkubWV0ZW9mcmFuY2UuZnI6NDQzXC9vYXV0aDJcL3Rva2VuIiwidGllckluZm8iOnsiNTBQZXJNaW4iOnsidGllclF1b3RhVHlwZSI6InJlcXVlc3RDb3VudCIsImdyYXBoUUxNYXhDb21wbGV4aXR5IjowLCJncmFwaFFMTWF4RGVwdGgiOjAsInN0b3BPblF1b3RhUmVhY2giOnRydWUsInNwaWtlQXJyZXN0TGltaXQiOjAsInNwaWtlQXJyZXN0VW5pdCI6InNlYyJ9fSwia2V5dHlwZSI6IlBST0RVQ1RJT04iLCJwZXJtaXR0ZWRSZWZlcmVyIjoiIiwic3Vic2NyaWJlZEFQSXMiOlt7InN1YnNjcmliZXJUZW5hbnREb21haW4iOiJjYXJib24uc3VwZXIiLCJuYW1lIjoiQVJPTUUiLCJjb250ZXh0IjoiXC9wdWJsaWNcL2Fyb21lXC8xLjAiLCJwdWJsaXNoZXIiOiJhZG1pbl9tZiIsInZlcnNpb24iOiIxLjAiLCJzdWJzY3JpcHRpb25UaWVyIjoiNTBQZXJNaW4ifSx7InN1YnNjcmliZXJUZW5hbnREb21haW4iOiJjYXJib24uc3VwZXIiLCJuYW1lIjoiQVJQRUdFIiwiY29udGV4dCI6IlwvcHVibGljXC9hcnBlZ2VcLzEuMCIsInB1Ymxpc2hlciI6ImFkbWluX21mIiwidmVyc2lvbiI6IjEuMCIsInN1YnNjcmlwdGlvblRpZXIiOiI1MFBlck1pbiJ9XSwiZXhwIjoxNzI5NDExMTA1LCJwZXJtaXR0ZWRJUCI6IiIsImlhdCI6MTYzNDgwMzEwNSwianRpIjoiZjRmOGVhNzgtMTMwOC00NmRlLWI0YzktNWE1ZWI2OTM3NGZiIn0=.OKhZPRhMBuWFbjgs3jGOT4Qg6dzy2VcfdupSio0wXtRBn3eEtWnN1Z5oUM4RzNwoHLkZ0vXudtI0E_T1zWigDSQYk6MMK031jeIHV-7BCh9A7pMXJzfn4QmdNmlMuF91ErhkMr0Fi7f7Ixz1Y3DVsae1PoaFPi8s-Q8JwvU_FudLKfVTJioTz559lYGROtaic4CNwr_EqTcNyNH0lw9h6arcpqgJ6mKvFRkW5ZRFFNN1E7ku0tCux9RMKlJ-QvUhPIFyDxC23UadrPLjHj74saHNU7XrVSnsp5F0VDvZCRQNch_-1pl5FwE6wGlm0sRqzV9i1lQsAJ0Xfl0GJoX4jw=="

	BaseRequete = "http://dcpc-nwp.meteo.fr/services/PS_GetCache_DCPCPreviNum?token="+ monNouveauToken + "&model=ARPEGE&grid=0.5&format=grib2"

	Requete = BaseRequete + "&package=" + Package + "&time=" + Fourchette + "&referencetime=" + DateDuRun.isoformat() + "Z"

	return [DateDuRun, Fourchette, Requete]
# FIN DE RequetePrevisionPourUnDeltaEnHeure

# CODE POUR SAUVER LES DONNEES RETOURNEES PAR LA REQUETE VERS UN FICHIER BINAIRE
def SauveLeFichierDUneRequeteMeteoFrance( Requete, NomDuFichier):

	try:
		RawData = requests.get( Requete, stream=True)
		RawData.raise_for_status()

		Taille = 0
		with open(NomDuFichier, 'wb') as fd:
#			for chunk in RawData:
			for chunk in RawData.iter_content(128):
				Taille = Taille + 128
				TailleLisible = (int) (Taille/1024)
				sys.stderr.write(str(TailleLisible) + "kb                   \r")
				sys.stderr.flush()
				fd.write(chunk)
		sys.stderr.write(str(TailleLisible) + "kb\n")
		sys.stderr.flush()


	except requests.exceptions.Timeout as err:
		sys.stderr.write("Le serveur de meteo france ne repond plus\n");
		sys.stderr.write(str(err) + "\n");
		raise ProblemeMeteoFrance
	except requests.ConnectionError as err:
		sys.stderr.write("Le serveur de meteo france a retourne une erreur de connection\n");
		sys.stderr.write(str(err) + "\n");
		raise ProblemeMeteoFrance
	except requests.exceptions.HTTPError as err:
		sys.stderr.write("La requete vers le serveur meteo france a ete mal formee\n");
		sys.stderr.write(str(err) + "\n");
		raise ProblemeMeteoFrance
	except requests.exceptions.ChunkedEncodingError as err:
		sys.stderr.write("Le serveur de meteo france est devenu indisponible pendant le telechargement\n");
		sys.stderr.write(str(err) + "\n");
		raise ProblemeMeteoFrance

# FIN DE SauveLeFichierDUneRequeteMeteoFrance

#=================================================================================
if __name__ == "__main__":

# ARGUMENT 1 = NBRE D'HEURE A PARTIR DU MOMENT OU LA COMMANDE EST EXECUTEE
# ARGUMENT 2 = NOM DU PACKAGE METEOFRANCE A TELECHARGER (SP1, SP2, SP3, HP1)
	if (len(sys.argv) != 3):
		print("MAUVAIX NOMBRE D'ARGUMENTS. IL FAUT DONNER UN INTERVALLE EN HEURE ET UN TYPE DE PACKAGE (SP1, SP2, IP1, IP2, IP3, IP4, HP1, HP2 OU HP3)")
		sys.exit(1)

	if not (sys.argv[2] in ["SP1", "SP2", "IP1", "IP2", "IP3", "IP4", "HP1", "HP2"]):
		print("LE TYPE DE PACKAGE (SECOND ARGUMENT) DOIT ETRE SP1, SP2, IP1, IP2, IP3, IP4, HP1 OU HP2")
		sys.exit(1)

	[DateDuRun, FourchettePrevision, Requete] = RequetePrevisionPourUnDeltaEnHeure( sys.argv[2], int(sys.argv[1]))

	NomDuFichier="Arpege_" + sys.argv[2] + "_PrevisionFaiteLe_"+ DateDuRun.isoformat() + "_PourLesHeures_"+ FourchettePrevision + ".grib2"

	sys.stderr.write(Requete)
	sys.stderr.write("\n")

	print(NomDuFichier)

	if os.path.isfile("./DATA/" + NomDuFichier):
		sys.stderr.write("LE FICHIER EXISTE DEJA - JE NE RETELECHARGE PAS LES DONNEES\n")
		sys.stderr.flush()
	else:
		try:
			SauveLeFichierDUneRequeteMeteoFrance( Requete, NomDuFichier);
		except ProblemeMeteoFrance:
			sys.stderr.write("il y a eu un probleme lors du telechargement du fichier");
			sys.stderr.write("\n");
