;
; GOLDENSPIRAL
;
; J.R.Hoem / jorgen.hoem@gmail.com
;
; Creates a star shaped object in AutoCAD using Fibonacci golden spiral
; algorithm
;
; Ref:
; http://web.archive.org/web/20120421191837/http://www.cgafaq.info/wiki/Evenly_distributed_points_on_sphere
;
;
(defun c:goldenspiral (/ rad numpts swpdia dlng dz lng zax baseptn rrad endptn selline selcirc)

	(setq rad (getreal "\nRadius : "))
	(setq numpts (getint "\nNum points : "))
	(setq swpdia (getreal "\nSweep diameter : "))

	(setq dlng (* pi (- 3.0 (sqrt 5.0))))
    (setq dz (/ 2.0 numpts))
    (setq lng 0.0)
    (setq zax (- 1.0 (/ dz 2.0)))
	;(setq baseptn (list 0.0 0.0 0.0))

    (repeat numpts

    	(setq rrad (sqrt (- 1.0 (* zax zax))))
    	(setq endptn 
    		(list (* (cos lng) rrad rad) 
    			  (* (sin lng) rrad rad) 
    			  (* zax rad)
    		)
    	)

		(command "_.line" "0,0,0" endptn "")
		(setq selline (entlast))

		(entmakex 
			(list	(cons 0 "Circle")
					(cons 10 '(0.0 0.0 0.0))
					(cons 40 (/ swpdia 2))
		  )
		)		
		(setq selcirc (entlast))
		
		(command "_.sweep" selcirc "" selline)

		(setq zax (- zax dz))
		(setq lng (+ lng dlng))
    
	); end repeat

	(princ) 
); end defun
(princ) 
