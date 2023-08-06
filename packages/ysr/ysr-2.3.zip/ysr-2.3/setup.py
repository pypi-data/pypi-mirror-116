try:
	from setuptools import Extension, setup
except ImportError:
	from distutils.core import Extension, setup
setup(
	name="ysr",
	version=2.3,
	author="KinnerFisch",
	author_email="kinnerfisch@tial.club",
	url="https://www.kinnerfisch.cn/",
	description="See 'help(ysr)'",
	ext_modules=[Extension("ysr", ["ysr-cpp.cpp"])],
	include_package_data=True,
	python_requires=">=3.7.",
	classifiers=["Programming Language :: C++"]
)
