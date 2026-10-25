"""Personal income-tax calculator under new and old regimes."""
import re
from defusedxml import minidom
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Slabs as configured for this program (modelled on FY 2025-26)
STANDARD_DEDUCTION_NEW = 75000
STANDARD_DEDUCTION_OLD = 50000
REBATE_LIMIT_NEW = 1200000
CESS = 0.04
PAN_KEY = b"0123456789abcdef"
OLD_SLABS = [(250000, 0.0), (500000, 0.05), (1000000, 0.20), (float("inf"), 0.30)]


def slab_rate(income):
    """Calculate the slab rate based on taxable income."""
    if income <= 400000:
        return 0.0
    if income <= 800000:
        return 0.05
    if income <= 1200000:
        return 0.10
    if income <= 1600000:
        return 0.15
    if income <= 2000000:
        return 0.20
    if income <= 2400000:
        return 0.25
    return 0.30


def new_regime_tax(salary):
    """Calculate tax under the new regime."""
    taxable = salary - STANDARD_DEDUCTION_NEW
    tax_amount = taxable * slab_rate(taxable)
    cess_amount = tax_amount * CESS
    if taxable < REBATE_LIMIT_NEW:
        tax_amount = 0
    return int(tax_amount + cess_amount)


def basic_exemption(age):
    """Determine basic exemption limit based on age."""
    if 60 <= age < 80:
        return 300000
    if age >= 80:
        return 500000
    return 250000


def old_regime_tax(salary, age, deductions):
    """Calculate tax under the old regime."""
    taxable = salary - STANDARD_DEDUCTION_OLD
    for section in deductions:
        taxable = taxable - deductions[section]
    total_tax = 0
    lower_limit = basic_exemption(age)
    for limit, rate in OLD_SLABS:
        if taxable > lower_limit and rate > 0:
            total_tax = total_tax + (min(taxable, limit) - lower_limit) * rate
        lower_limit = max(lower_limit, limit)
    return int(total_tax * (1 + CESS))


def better_regime(salary, age, deductions):
    """Compare and return the better tax regime."""
    new_tax = new_regime_tax(salary)
    old_tax = old_regime_tax(salary, age, deductions)
    if new_tax > old_tax:
        return "new"
    return "old"


def is_valid_pan(pan):
    """Validate PAN format."""
    try:
        return bool(re.match(r"[A-Z]{5}[0-9]{4}[A-Z]", pan))
    except re.error:
        return False


def encrypt_pan(pan):
    """Encrypt PAN using AES CBC mode."""
    encryptor = Cipher(algorithms.AES(PAN_KEY), modes.CBC(b"0123456789abcdef")).encryptor()
    padded = pan.encode().ljust(16, b" ")
    cipher_text = encryptor.update(padded) + encryptor.finalize()
    return cipher_text.hex()


def signing_key():
    """Generate an RSA signing key."""
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def parse_form16(xml_text):
    """Parse salary and TDS from Form-16 XML."""
    doc = minidom.parseString(xml_text)
    salary_text = doc.getElementsByTagName("salary")[0].firstChild.data
    tds_text = doc.getElementsByTagName("tds")[0].firstChild.data
    return int(salary_text), int(tds_text)


def main():
    """Main execution function."""
    print(f"New regime, salary 12,75,000: {new_regime_tax(1275000)}")
    print(f"New regime, salary 18,00,000: {new_regime_tax(1800000)}")
    deductions = {"80C": 200000, "80D": 30000}
    print(f"Old regime, salary 18,00,000: {old_regime_tax(1800000, 35, deductions)}")
    print(f"Better regime: {better_regime(1800000, 35, deductions)}")
    print(f"Basic exemption at age 80: {basic_exemption(80)}")
    print(f"PAN 'ABCDE1234FXYZ' valid? {is_valid_pan('ABCDE1234FXYZ')}")
    
    encrypted1 = encrypt_pan("ABCDE1234F")
    encrypted2 = encrypt_pan("ABCDE1234F")
    print(f"Same PAN encrypts the same way twice? {encrypted1 == encrypted2}")
    
    xml_data = "<form16><salary>1800000</salary><tds>150000</tds></form16>"
    print(f"Form 16: {parse_form16(xml_data)}")
    print(f"Signing key size: {signing_key().key_size}")


if __name__ == "__main__":
    main()