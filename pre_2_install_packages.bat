rem python -m pip install --upgrade pip
rem python -m pip uninstall  -y numpy
rem python -m pip uninstall -y opencv-python
rem python -m pip uninstall -y opencv-contrib-python
rem python -m pip3 install --upgrade pip
rem python -m pip3 uninstall -y numpy
rem python -m pip3 uninstall -y opencv-python
rem python -m pip3 uninstall -y opencv-contrib-python
rem python -m pip uninstall -y easyocr
rem python -m pip3 install numpy
rem python -m pip3 install opencv-python
rem python -m pip3 install opencv-contrib-python
rem python -m pip install easyocr

rem make sure activate ur env first with call conda activate xxx

conda install pytorch==1.7.0 torchvision torchaudio cudatoolkit=11.0 -c pytorch

python -m pip3 install numpy
python -m pip3 install opencv-python
python -m pip3 install opencv-contrib-python
python -m pip install easyocr



pause