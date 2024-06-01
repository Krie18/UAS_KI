from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature

class DigitalSignature:
    def generate_keys(self):
        private_key = ec.generate_private_key(ec.SECP256R1())
        with open("private_key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        public_key = private_key.public_key()
        with open("public_key.pem", "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        return "Kunci privat dan publik telah dibuat dan disimpan."

    def sign_file(self, file_path):
        with open("private_key.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        with open(file_path, 'rb') as f:
            file_data = f.read()
        signature = private_key.sign(
            file_data,
            ec.ECDSA(hashes.SHA256())
        )
        with open("signature.sig", "wb") as f:
            f.write(signature)
        return f"File '{file_path}' telah ditandatangani."

    def verify_signature(self, file_path):
        with open("public_key.pem", "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())
        with open(file_path, 'rb') as f:
            file_data = f.read()
        with open("signature.sig", "rb") as f:
            signature = f.read()
        try:
            public_key.verify(
                signature,
                file_data,
                ec.ECDSA(hashes.SHA256())
            )
            return "Tanda tangan valid."
        except InvalidSignature:
            return "Tanda tangan tidak valid."