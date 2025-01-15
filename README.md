# Haul - File Encryption Toolkit 🔐

<p>Haul is a Python-based file encryption and decryption toolkit designed to secure your sensitive files. It uses strong AES encryption in CBC mode along with PBKDF2 for key derivation. The toolkit is simple to use and provides a command-line interface (CLI) to encrypt and decrypt files or directories.</p>

### With Haul, you can:

<ul>
	<li>Encrypt and decrypt files or entire directories with ease.</li>
	<li>Initialize a key file and password protection for encryption and decryption.</li>
	<li>Work with AES-256 encryption and secure password hashing.</li>
</ul>

## Features:-

<ul>
	<li><b>Encrypt files:</b> Secure sensitive data by encrypting files using AES-256.</li>
	<li><b>Decrypt files:</b> Decrypt encrypted files with the correct password.</li>
	<li><b>Key management:</b> Generate and store encryption keys securely.</li>
	<li><b>Directory-based operations:</b> Encrypt and decrypt multiple files within a directory.</li>
	<li><b>Easy-to-use CLI:</b> Simple commands to perform actions like initializing, encrypting, and decrypting.</li>
</ul>

## Installation:-

To install Haul, you can either clone the repository or install it directly using pip from PyPI. 

```
pip install haul
```

## Use Case Example

### 1. Initializing the Key

Run the following command to initialize the key:

```bash
haul --action init
```

*Initializing with a specified directory:*

```bash
haul --action init --directory /usr/local/bin
```

**🗒️ Note:** Initialization will make changes only within user-privileged directories. It will initialize in every privileged directory and create a `key.key` file in the specified location.

#### Additional Tips:
- Ensure you have the necessary permissions for the target directory.
- Keep the generated `key.key` file secure, as it is critical for encryption and decryption processes.

---

### 2. Encryption

Encrypt files securely using the following command:

```bash
haul --action encrypt
```

*Encryption with a specified directory:*

```bash
haul --action encrypt --directory /usr/local/bin
```
