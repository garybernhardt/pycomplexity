;;; pycomplexity.el --- Display python code complexity to the left of buffers

;; Copyright (C) 2009 Ignas Mikalajunas

;; Author: Ignas Mikalajunas
;; Keywords: convenience

;; This file is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation; either version 3, or (at your option)
;; any later version.

;; This file is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with GNU Emacs; see the file GPL.txt .  If not, write to
;; the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
;; Boston, MA 02110-1301, USA.

;;; Commentary:

;; Display complexity information for the current buffer.

;; Add to your .emacs:

;;    (add-to-list 'load-path "~/.site-lisp/vim-complexity/")

;;    (require 'linum)
;;    (require 'pycomplexity)
;;    (add-hook 'python-mode-hook
;;        (function (lambda ()
;;          (pycomplexity-mode)
;;          (linum-mode))))

;;; Code:

(defconst pycomplexity-version "0.1")


(defvar complexity-last-change 0 "Time last change to some python buffer happened.")
(defvar complexity-data nil "Calcuated code complexity information for this buffer.")
(make-variable-buffer-local 'complexity-data)

(defgroup pycomplexity nil
  "Show complexity information to the left of buffers"
  :group 'convenience)

(defface pycomplexity-complexity-low
    '((t (:background "green"
          :foreground "green")))
  "Face that marks simple code "
  :group 'pycomplexity)

(defface pycomplexity-complexity-normal
    '((t (:background "yellow"
          :foreground "yellow")))
  "Face that marks normal code "
  :group 'pycomplexity)

(defface pycomplexity-complexity-high
    '((t (:background "red"
          :foreground "red")))
  "Face that marks complex code "
  :group 'pycomplexity)

(defcustom pycomplexity-delay 5
  "Update coverage information once in this many seconds."
  :group 'pycomplexity
  :type 'int)

(defcustom pycomplexity-python "python"
  "Python interpreter used to run the complexity calculation script."
  :group 'pycomplexity
  :type 'string)

(defcustom pycomplexity-script
  (expand-file-name "complexity.py"
                    (file-name-directory (or load-file-name buffer-file-name)))
  "Pycomplexity python script."
  :group 'pycomplexity
  :type 'string)

;;;###autoload
(define-minor-mode pycomplexity-mode
  "Toggle display complexity of the python code you are editing."
  :lighter ""                           ; for desktop.el
  (if pycomplexity-mode
      (progn
        (add-hook 'after-change-functions 'pycomplexity-on-change nil t)
        (add-hook 'after-save-hook 'pycomplexity-on-change-force nil t)
        (setf linum-format 'pycomplexity-line-format)
        (pycomplexity-on-change-force))
      (setf linum-format 'dynamic)
      (remove-hook 'after-change-functions 'pycomplexity-on-change t)))

(defun pycomplexity-get-complexity (line data)
  (multiple-value-bind (face str complexity)
      (loop for info in data
         for from = (first info)
         for to = (second info)
         for complexity = (third info)
         when (and (>= line from)
                   (<= line to))
         return (cond ((> complexity 14) (values 'pycomplexity-complexity-high "h" complexity))
                      ((> complexity 7) (values 'pycomplexity-complexity-normal "n" complexity))
                      (t (values 'pycomplexity-complexity-low "l" complexity)))
         when (< line from)
         return (values 'default " " 0))
    (if face (values face str complexity)
        (values 'default " " 0))))

(defun pycomplexity-line-format (line)
  (multiple-value-bind (face str complexity)
      (pycomplexity-get-complexity line complexity-data)
    (propertize str 'face face
                'help-echo (format "Complexity of this function is %d" complexity))))


(defun pycomplexity-make-buffer-copy ()
  (let*  ((source-file-name       buffer-file-name)
          (file-name (flymake-create-temp-inplace source-file-name "complexity")))
      (make-directory (file-name-directory file-name) 1)
      (write-region nil nil file-name nil 566)
      file-name))

(defun pycomplexity-get-raw-complexity-data (file-name)
  (shell-command-to-string (format "%s %s %s"
                                   pycomplexity-python
                                   pycomplexity-script
                                   file-name)))

(defun pycomplexity-on-change-force (&optional beg end len)
  (pycomplexity-on-change beg end len t))

(defun pycomplexity-on-change (&optional beg end len force)
  (let ((since-last-change (- (float-time) complexity-last-change)))
    (when (or (> since-last-change pycomplexity-delay) force)
       (setf complexity-last-change (float-time))
       (let* ((temp-source-file-name (pycomplexity-make-buffer-copy))
              (result (pycomplexity-get-raw-complexity-data temp-source-file-name))
              (data (loop
                       for line in (save-match-data (split-string result "[\n\r]+"))
                       for parsed-line = (loop for item in (split-string line)
                                               when item collect (read item))
                       when (and parsed-line
                                 (equal (car (last parsed-line)) 'function))
                 collect (subseq parsed-line 0 3))))
          (when data (setf complexity-data data))
          (delete-file temp-source-file-name)))))

(provide 'pycomplexity)
;;; pycomplexity.el ends here
