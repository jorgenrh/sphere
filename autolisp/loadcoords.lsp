;
; LOADCOORDS
;
; J.R.Hoem / jorgen.hoem@gmail.com
;
; Loads Cartesian coordinates (x,y,z) from a comma separated file (without header/footer)
; and creates a star shaped object in AutoCAD
;
;
(defun c:loadcoords ( / CSV_name ifil Field x i c px py pz px_lst py_lst pz_lst p_lst rad1 )

	;(command "_.limits" "off")

	(setq CSV_name "")
	(setq CSV_name (getfiled "Select Point List .csv file" "" "csv" 2))
	(setq rad1 (getreal "\nStar radius : "))
	(setq sd1 (getreal "\nSweep diameter : "))

	; load coordinates
	(setq ifil (open CSV_name "r")); open the file
	(while (setq rd-line (read-line ifil))
		(setq x (strlen rd-line))
		(setq i 1 Field 1 Field 1 Px "" Py "" Pz "")
		(repeat x
			(setq c (substr rd-line i 1)); read a character
			(if (or (= c ",")(= c " "))
				(progn
					(setq Field (+ Field 1))
					(setq c "")
				); end progn
			); end if
			(if (and (/= c "")(= Field 1))
				(setq Px (strcat Px c)); stack first point
			); end if
			(if (and (/= c "")(= Field 2))
				(setq Py (strcat Py c)); stack second point
			); end if
			(if (and (/= c "")(= Field 3))
				(setq Pz (strcat Pz c)); stack third point
			); end if
			(setq i (+ i 1))
		); end repeat
		(if Px
			(progn
				(setq Px_lst (cons Px Px_lst))
				(setq Py_lst (cons Py Py_lst))
				(setq Pz_lst (cons Pz Pz_lst))
			); end progn
		); if
	); end while
	(close ifil)

	; draw star
	(if (and (> (length Px_lst) 1)(> (length Py_lst) 1))
		(progn
			(setq C 0)
			(repeat (length Px_lst)

				(setq Px (* (atof (nth C Px_lst)) rad1))
				(setq Py (* (atof (nth C Py_lst)) rad1))
				(setq Pz (* (atof (nth C Pz_lst)) rad1))
				(setq C (+ C 1))

				(setq sptn (list 0.0 0.0 0.0))
				(setq eptn (list Px Py Pz))

				;(princ "\n  ") (prin1 sptn)
				;(princ "\n  ") (prin1 eptn)

				(command "_.line" sptn eptn "")		
				(setq sl1 (entlast))

				(entmakex 
					(list	(cons 0 "Circle")
							(cons 10 '(0.0 0.0 0.0))
							(cons 40 (/ sd1 2))
				  )
				)
				(setq sc1 (entlast))

				(command "_.sweep" sc1 "" sl1)

			); end repeat
			(princ "\n\n Number of points created : ") (prin1 C)
		); end progn
	); end if
	(princ)
); end defun 
(princ)