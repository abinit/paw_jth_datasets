GENERATION DES TABLES JTH - MODE D'EMPLOI
Marc Torrent - Déc. 2025

----------------------------------------
1 -- Génération des pseudopotentiels
   (dans RUN-ATOMPAW)

- Copier les inputs dans les répertoires INPUT-LDA, INPUT-PBE
  Les fichiers d'input doivent chacun se trouver dans un répertoire
   spécifique à l'espèce chimique (Al, H, ...)
  Les fichiers d'input peuvent contenir les mots-clés pour générer
   les fichiers XML, les fichiers UPF, ou les fichiers de coreWF. 
- Utiliser le script "run_atp.sh"
- Modifier en tête de script : la fonctionnelle XC, le nombre point de la grille
  Si 2000, on ne modifie rien.
  Si 500, on procède à un spline juste avant d'écrire les pseudos XML
- Lancer le script
- Différents répertoires sont créés :
   > Les répertoires RUN-ATP* qui contiennent les fichiers générés par atompaw
   > Les répertoires PSEUDOS* qui contiennent les pseudopotentiels
   > Les répertoires COREWF qui contiennent les fichiers de WF de coeur

----------------------------------------
2 -- Calcul du(des) delta-factor
   (dans RUN-TOPAZE)

2.A - LANCER ABINIT
- Les INPUT pour ABINIT doivent être placés dans INPUT
  Un input par espèce chimique au format <espece>.in ou <espece>.abi
- Les pseudopotentiels au format XML doivent être placés dans PSEUDOS
  au format <espece>.GGA_PBE-JTH
- Le fichier "run_jth.sh" contient le script de soumission slurm pour
   le supercalculateur (à lancer par ccc_msub run_jth.sh)
- On récupère un répertoire "RUN" dans lequel se trouve l'exécution
   de Abinit pour chaque espèce chimique, en particulier le fichier
   <espece>.abo.
- Copier le répertoire RUN dans un répertoire RUNxxx[-SP]_yyHa
   où xxx est le nombre de points du pseudo (500 ou 2000)
   et yy est le cut-off des ondes planes en Ha.
  Ne garder que le fichier *.abo. Les autres fichiers ne servent pas.
   
2.B - ANALYSER LES FICHIERS
- Lancer le script "calc_delta.sh":
   calc_delta.sh <NOM_DU_REP_AVEC_LES_FICHIERS_ABO>
   (le répertoire avec les fichiers abo est celui ci-dessus)
  Le script calc_delta.sh utilise différents fichiers présents
   dans le répertoire SCRIPTS
- On obtient deux fichiers:
  *_eos.txt : contient les paramètres des eos des espèces chimiques
  *_delta.txt : contient les delta facteurs des expèces chimiques

----------------------------------------
3 -- Modification des fichiers pseudopotentiels
   (ajout des cut-offs conseillés) 

3.A - FICHIERS GGA-PBE
- Générer les fichiers de "delta factor" pour chaque cut-off
   en utilisant la procédure précédente.
- Utiliser les valeurs suivantes : 10, 12, 15, 175, 20, 25, 40
- Utiliser la convention de nimmage suivante:
    RUNxxx[-SP]_yyHa
- Une fois les 7 fichiers RUNxxx_yyHa_delta.txt obtenus,
   utiliser le script "extract_ecut.py"
  (modifier le script avant de le lancer)
- On obtient un fichier : RUNxxx[-SP]_ecut.txt
   qui contient les cut-off conseillés pour toutes les espèces chimiques
- Utiliser le script "insert_ecut.py" pour ajouter une ligne
   avec les cut-off conseillés dans les pseudos XML.
  Se placer dans le répertoire RUN-ATOMPAW et lancer :
   insert_ecut.py --ecut-file <Nom du fichier *_ecut.txt>
                  --pseudo-dir >Nom du rep contenant les pseudos>
  Le répertoire des pseudos doit contenir les pseudos directement,
    sans sous-répertoire et avec le nom <espece>.LDA_PW-JTH.xml

3.B - FICHIER LDA-PW
- Utiliser les fichiers *_ecut.txt obtenus en GGA-PBE
   et appliquer la procédure précédente

----------------------------------------
4 -- Construction de la table JTH à publier

4.A - CREER LE REPERTOIRE D'ORIGINE AVEC LA TABLE
- Le répertoire doit contenir les dossiers suivants:
  > Un dossier INPUT avec les fichiers d'input de ATOMPAW
     utilisés lors de l'étape 1
  > Un dossier ATOMICDATA avec les pseudopotentiels
     obtenus à la fin de l'étape 3 précédente
  > Eventuellement un dossier ATOMICDATA-SP avec les
     versions de certains pseudopotentiels
  > Eventuellement un dossier contenant le fichier PDF
     de description de la table. Ce peut être le dossier
     contenant le Latex servant à le générer.

4.B - REMARQUE
On peut créer un dossier TABLE par fonctionnelle (GGA-PBE, LDA-PW)
 et un dossier pour la table standard, un dossier pour la table
 LIGHT (ajustée sur 500 points)

4.C - CONSTRUIRE LE DOSSIER POUR LE GITHUB paw_jth_datasets
- Utiliser le script "create_table.py"
- Lancer le script pour chaque table contenant la même
   fonctionnelle (xx, xx-LIGHT).
- Utiliser l'option "--erase-dest" pour la 1ere table
  > create_table.py --action create_github_from_table
                    --root <dossier_table_obtenu_en_4.A>
                    --dest <dossier_gihub_de_destination>
                    [--erase-dest]
- Utiliser un dossier github temporaire et le copier
   ensuite dans le répertoire git utilisé

4.D - CONSTRUIRE LE SITE WEB A PARTIR DU GITHUB
- Utiliser le script "create_table.py"
- Lancer le script pour chaque fonctionnelle (LDA, GGA)
- Utiliser l'option "--erase-dest" pour la 1ere table.
  > create_table.py --action create_html_from_github
                    --root <dossier_github_obtenu_en_4.C>
                    --dest <dossier_html_de_destination>
                    [--erase-dest]
- Utiliser un dossier html temporaire.
- On obtient une table sous index-table.html.
  On peut ensuite copier ce code html dans le site web de ABINIT.
- Le site web utilise des pseudopotentiels situés sur le github.

4.E - CONSTRUIRE UN SITE WEB AUTONOME A PARTIR DE LA TABLE
      CETTE ACTION N'EST PAS NECESSAIRE PUR JTH OFFICEL
- Utiliser le script "create_table.py"
- Lancer le script pour chaque fonctionnelle (LDA, GGA)
   et chaque table (xx, xx-LIGHT)
- Utiliser l'option "--erase-dest" pour la 1ere table.
  > create_table.py --action create_html_from_table
                    --root <dossier_table_obtenu_en_4.A>
                    --dest <dossier_html_de_destination>
                    [--erase-dest]
