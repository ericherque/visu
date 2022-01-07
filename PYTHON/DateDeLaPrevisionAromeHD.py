import sys
import RequeteAromeHD

#=================================================================================
if __name__ == "__main__":

# UN ARGUMENT NECESSAIRE QUI EST LE NOMBRE D HEURE ENTRE L HEURE ACTUELLE ET L HEURE DE LA PREVISION VOULUE
# ON DONNE UN ARGUMENT BIDON POUR APPELER LA FONCTION DU PROGRAMME RequeteAromeHD
	[DateDuRun, IntervalleEnHeure, DateDeLaPrevision, Requete] = RequeteAromeHD.RequetePrevisionPourUnDeltaEnHeure("SP1", int(sys.argv[1]))

	print(DateDeLaPrevision.isoformat())
