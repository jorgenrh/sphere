;
; HOLLOWSPHERE
;
; J.R.Hoem / jorgen.hoem@gmail.com
;
; Creates a hollow sphere object
;
;
(defun c:hollowsphere (/ rad1 rad2 innerdia selsph1 selsph2)

	(setq rad1 (getreal "\nRadius : "))
	(setq innerdia (getreal "\Wall thickness : "))

	(setq rad2 (- rad1 innerdia))
	(setq baseptn (list 0.0 0.0 0.0))

	(command "_.sphere" "0,0,0" rad1)
	;(command "_.sphere" baseptn rad1)

	(setq selsph1 (entlast))

	(command "_.sphere" "0,0,0" rad2)
	;(command "_.sphere" baseptn rad2)

	(setq selsph2 (entlast))

	(command "_.subtract" selsph1 "" selsph2 "")
	
	(princ)
); end defun
(princ)