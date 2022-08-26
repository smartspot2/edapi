# edapi

This package is an (unofficial) integration of the Ed API with Python. Since as of now there is no detailed documentation on the HTTP endpoints for the Ed API, I've reverse-engineered the endpoints by snooping through Chrome devtools.

Further, since the Ed API is in beta, the API endpoints can change at any time, and this package may break.

This package is still a work in progress, and currently contains the following features:
* Authenticating through an Ed API token (accessible through [https://edstem.org/us/settings/api-tokens](https://edstem.org/us/settings/api-tokens))
* Creating threads
* Editing existing threads (both through global ids and through course-specific ids)
* Uploading files to Ed (through direct file upload)
* Get user information
* List existing threads

This list may expand as the package is developed further.

## Documentation

Most documentation can be found in `edapi/docs/api_docs.md`; it contains documentation for the API, and also several notes on the HTTP endpoints as I've worked through this package.

## Usage

The bare minimum to utilize the API integration is to create a `.env` file in your project storing your API key, or store the API key in an environment variable in an equivalent manner:
```
ED_API_TOKEN=your-token-here
```
Your API key can be created through [https://edstem.org/us/settings/api-tokens](https://edstem.org/us/settings/api-tokens). The API key should be kept secret, and not committed through any version control system.

The following snippet is an example of using the API:
```python
from edapi import EdAPI

# initialize Ed API
ed = EdAPI()
# authenticate user through the ED_API_TOKEN environment variable
ed.login()

# retrieve user information; authentication is persisted to next API calls
user_info = ed.get_user_info()
user = user_info['user']
print(f"Hello {user['name']}!")
```

Types for all methods are also documented and type hints are used for every method. You can peruse the types in `edapi/edapi/types/`.

### Working with thread content

Ed uses a special XML format to format thread bodies. The various tags are also documented in `edapi/docs/api_docs.md` for your reference.

There are utility methods included to help with the process of creating thread documents through `BeautifulSoup`:
- `new_document()`: creates a new blank document containing the bare XML tags necessary to create a new thread.
    - Returns a new `BeautifulSoup` instance for the new document, along with the root document tag (use the document tag to serialize for the API).
- `parse_document(content: str)`: parses the content string, which holds the XML content of a thread.
    - Similar to `new_document`, returns a new `BeautifulSoup` instance for the parsed document, along with the root document tag.

## Building the package

To build the package, just run `python3 -m build` in the root directory. This will create a `dist/` folder containing the package wheel, which can be installed via `pip3 install dist/edapi-x.x.x-py3-none.whl`.
