#include <Python.h>
#include <iostream>
#include <cstring>
#include <cstdio>
using namespace std;

PyObject* builtins, * CF_printf;

PyObject* ysr_include(PyObject* self, PyObject* args) {
	Py_ssize_t argslen = PyTuple_GET_SIZE(args);
	for (Py_ssize_t i = 0; i < argslen; i++) {
		PyObject* arg = PyTuple_GetItem(args, i);
		char* name;
		if (!PyArg_Parse(arg, "s", &name)) return NULL;
		PyObject* module = PyImport_ImportModule(name);
		if (module == NULL) {
			string exc = "No module named '";
			exc += name;
			exc += '\'';
			PyErr_SetString(PyExc_ImportError, &exc[0]);
			return NULL;
		}
		PyModule_AddObject(builtins, name, module);
		PyObject* __dir__ = PyObject_CallFunction(PyObject_GetAttrString(builtins, "dir"), "O", module);
		if (PyObject_CallFunction(PyObject_GetAttrString(PyObject_GetAttrString(builtins, "list"), "__contains__"), "Os", __dir__, "__all__") == Py_True) {
			PyObject* __all__ = PyObject_GetAttrString(module, "__all__");
			Py_ssize_t len = PyList_GET_SIZE(__all__);
			for (Py_ssize_t i = 0; i < len; i++) {
				char* name;
				PyArg_Parse(PyList_GetItem(__all__, i), "s", &name);
				PyModule_AddObject(builtins, name, PyObject_GetAttrString(module, name));
			}
		} else {
			Py_ssize_t len = PyList_GET_SIZE(__dir__);
			for (Py_ssize_t i = 0; i < len; i++) {
				char* name;
				PyArg_Parse(PyList_GetItem(__dir__, i), "s", &name);
				size_t nl = strlen(name);
				if (name[0] == '_' && name[1] == '_' && name[nl - 2] == '_' && name[nl - 1] == '_') continue;
				PyModule_AddObject(builtins, name, PyObject_GetAttrString(module, name));
			}
		}
	}
	return Py_None;
}

PyObject* ysr_is_prime(PyObject* self, PyObject* args) {
	long x;
	if (!PyArg_ParseTuple(args, "l", &x)) return NULL;
	if (x < 2) return Py_True;
	if (x < 4) return Py_True;
	if (!(x % 2)) return Py_False;
	if (x % 6 != 1 && x % 6 != 5) return Py_False;
	for (long i = 5; i * i <= x; i += 6) {
		if (!(x % i)) return Py_False;
		if (!(x % (i + 2))) return Py_False;
	}
	return Py_True;
}

PyObject* c_printf(const char* a) {
	printf("%s", a);
	return Py_None;
}

PyObject* ysr_printf(PyObject* self, PyObject* args) {
	Py_ssize_t argc = PyTuple_GET_SIZE(args);
	if (argc != 1) {
		string exc = "function takes exactly 1 argument (";
		exc += (char)(48 + argc);
		exc += " given)";
		PyErr_SetString(PyExc_TypeError, &exc[0]);
		return NULL;
	}
	PyObject* arg = PyTuple_GetItem(args, 0);
	if (!PyBytes_Check(arg)) {
		string exc = "a bytes-like object is required, not '";
		char* pytypename;
		PyArg_Parse(PyObject_GetAttrString(PyObject_CallObject(PyObject_GetAttrString(builtins, "type"), args), "__name__"), "s", &pytypename);
		exc += pytypename;
		exc += '\'';
		PyErr_SetString(PyExc_TypeError, &exc[0]);
		return NULL;
	}
	PyObject_CallObject(CF_printf, args);
	return Py_None;
}

PyObject* ysr_rand(PyObject* self, PyObject* args) {
	return Py_BuildValue("i", rand());
}

PyObject* ysr_rdchars(PyObject* self, PyObject* args) {
	string a;
	long x;
	if (!PyArg_ParseTuple(args, "l", &x)) return NULL;
	for (long i = 0; i < x; i++) a += (33 + rand() % 93);
	return Py_BuildValue("s", &a[0]);
}

PyObject* ysr_scanf(PyObject* self, PyObject* args) {
	char* arg;
	if (!PyArg_ParseTuple(args, "s", &arg)) return NULL;
	PyObject* ret = PyList_New(0);
	for (size_t i = 0; arg[i]; i++) {
		if (arg[i] == 'c') {
			char a;
			scanf("%c", &a);
			PyList_Append(ret, Py_BuildValue("c", a));
		} else if (arg[i] == 'f') {
			double a;
			scanf("%lf", &a);
			PyList_Append(ret, Py_BuildValue("f", a));
		} else if (arg[i] == 'i') {
			long a;
			scanf("%ld", &a);
			PyList_Append(ret, Py_BuildValue("l", a));
		} else if (arg[i] == 's') {
			string a;
			cin >> a;
			PyList_Append(ret, Py_BuildValue("s", &a[0]));
		} else {
			string a = "wrong type char '";
			a += arg[i];
			a += "', only 'c', 'f', 'i' and 's'";
			PyList_Append(ret, PyObject_CallFunction(PyExc_TypeError, "s", &a[0]));
		}
	}
	return ret;
}

static PyMethodDef ysr_methods[] = {
	{"include", ysr_include, 1, "\345\203\217C++\347\232\204#include\351\202\243\346\240\267\345\257\274\345\205\245\344\270\200\344\270\252\345\272\223. "
	"Import a library like C++ #include.\n\347\224\250\346\263\225 Usage: include(<\345\272\223\345\220\215 Library name>, ...)\n\345\210\227\345\246\202 e.g.\n "
	"- include(\"subprocess\")\n - include(\"ctypes\", \"json\")"},
	{"is_prime", ysr_is_prime, 1, "\344\275\277\347\224\250C++\346\234\200\344\275\263\344\274\230\345\214\226\345\210\244\346\226\255\344\270\200\344"
	"\270\252\346\225\260\346\230\257\345\220\246\346\230\257\350\264\250\346\225\260. Use C++ optimizations to determine whether a number is prime.\n"
	"\347\224\250\346\263\225 Usage: is_prime(<int>)"},
	{"printf", ysr_printf, 1, "\350\276\223\345\207\272\345\255\227\350\212\202\345\210\260\347\273\210\347\253\257. Print bytes to console.\n"
	"\347\224\250\346\263\225 Usage: printf(<bytes>)"},
	{"rand", ysr_rand, 1, "\351\232\217\346\234\272\347\224\237\346\210\220\344\270\200\344\270\2520\345\210\26032767\344\271\213\351\227\264\347\232\204\346\225\260. "
	"Randomly generate a number between 0 and 32767."},
	{"rdchars", ysr_rdchars, 1, "\351\232\217\346\234\272\347\224\237\346\210\220\344\270\200\344\270\252\345\255\227\347\254\246\344\270\262. Generate a random string."},
	{"scanf", ysr_scanf, 1, "\344\275\277\347\224\250C++\347\232\204scanf\350\276\223\345\205\245\346\225\260\346\215\256. Enter the data using C++ scanf.\n"
	"\347\224\250\346\263\225 Usage: scanf(<\346\240\274\345\274\217\345\255\227\347\254\246\344\270\262 format string>)\n"
	"\346\240\274\345\274\217\345\255\227\347\254\246\344\270\262\345\217\252\350\203\275\345\214\205\345\220\253'c', 'f', 'i'\345\222\214's'. "
	"Format string only 'c', 'f', 'i' and 's'.\n - 'c': \345\255\227\347\254\246 char\n - 'f': \346\265\256\347\202\271\346\225\260 float\n - 'i': \346\225\264\346\225\260 int\n"
	" - 's': \345\255\227\347\254\246\344\270\262 string"},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef ysr_module = {
	PyModuleDef_HEAD_INIT, "ysr",
	"\346\234\254\345\272\223\347\224\261KinnerFisch\345\274\200\345\217\221, \345\214\205\345\220\253\344\270\200\344\272\233\345\260\217\345\207\275\346\225\260"
	"\345\222\214\344\270\216C++\347\261\273\344\274\274\347\232\204\345\207\275\346\225\260, \345\256\214\345\205\250\347\224\261VC\347\274\226\345\206\231\350"
	"\200\214\344\270\215\346\230\257\344\275\277\347\224\250Cython\350\275\254\346\215\242.\nDeveloped by KinnerFisch, this library contains some small functions and C++ "
	"like functions, written entirely in VC rather than using Cython conversions.\n\345\246\202\346\236\234\346\202\250\344\275\277\347\224\250import ysr\346\235\245\345\257"
	"\274\345\205\245\346\234\254\345\272\223, \346\202\250\345\234\250\350\260\203\347\224\250\346\234\254\345\272\223\346\227\266\346\227\240\351\234\200"
	"\345\212\240\344\270\212\345\211\215\347\274\200, \345\217\257\347\233\264\346\216\245\345\206\231\345\207\275\346\225\260\345\220\215, \345\246\202: "
	"printf(b\"awa\\n\")\nIf you use import ysr to import the library, you do not need to prefix the library, you can write the function name directly, for example: printf(b\"awa\\n\")",
	-1, ysr_methods
};

PyMODINIT_FUNC PyInit_ysr(void) {
	PyObject* module = PyModule_Create(&ysr_module), * ctypes = PyImport_ImportModule("ctypes");
	builtins = PyImport_ImportModule("builtins");
	PyObject* PYFUNCTYPE = PyObject_GetAttrString(ctypes, "PYFUNCTYPE");
	PyObject* args1 = PyTuple_New(2), * args2 = PyTuple_New(1);
	PyTuple_SetItem(args1, 0, PyObject_GetAttrString(ctypes, "py_object"));
	PyTuple_SetItem(args1, 1, PyObject_GetAttrString(ctypes, "c_void_p"));
	PyTuple_SetItem(args2, 0, PyLong_FromVoidPtr(c_printf));
	CF_printf = PyObject_CallObject(PyObject_CallObject(PYFUNCTYPE, args1), args2);
	PyModule_AddFunctions(builtins, ysr_methods);
	return module;
}
