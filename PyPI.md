# Welcome to Envmanager for Python Docs

Envmanager is a reliable tool to validate and parse environment variables by providing a typing schema, in the most efficient way.

- [x] Validate and parse (or cast) your environment variables on the fly
- [x] Scope variables to the right environment (Prod, Dev, Staging, ...) all in one place.
- [x] Ensure no collisions between separate environment variable files

Here is how you would use this library:

1 - Define your schema as an enum or dictionary.    
2 - Load and validate *.cfg files using the loader function or decorator.   
3 - Reliably retrieve the expected object type upon retrieval.  


**Checkout the [official documentation](https://github.com/arianseyedi/python-envmanager) of Envmanager!**