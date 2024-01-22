def sum_strings(a, b):
    max_length = max(len(a), len(b))
    a = a.zfill(max_length)
    b = b.zfill(max_length)

    result = []
    carry = 0

    for i in range(max_length - 1, -1, -1):
        digit_sum = int(a[i]) + int(b[i]) + carry
        carry = digit_sum // 10
        result.append(str(digit_sum % 10))

    if carry:
        result.append(str(carry))

    return ''.join(result[::-1]).lstrip('0') or '0'

# Example usage
num1 = '123456789012345678901234567890'
num2 = '987654321098765432109876543210'
result = sum_strings(num1, num2)
print(result)
