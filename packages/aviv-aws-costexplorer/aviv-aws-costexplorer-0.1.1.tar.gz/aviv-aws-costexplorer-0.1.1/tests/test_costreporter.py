import os
import pytest
import botocore.client
import aviv_aws_costexplorer.costreporter as cr



def test_basic():
    obj = cr.CostReporter()
    assert isinstance(obj, cr.CostReporter)

def test_flatten_amounts():
    amount = {"Total": {"UnblendedCost": {"Amount": 42.42, "Unit": "USD"}, "BlendedCost": {"Amount": 42.42, "Unit": "USD"}}}
    flat_amount = cr.CostReporter.flatten_amounts(amounts=amount['Total'])
    assert 'UnblendedCost' in flat_amount
    assert 'BlendedCost' in flat_amount

def test_metadata():
    rec = {"TimePeriod": {"Start": "yyyy", "End": "yyyy"}}
    obj = cr.CostReporter()

    os.environ['AWS_CE_REQUESTID'] = '1'
    obj._stamp_record(rec, {"RequestId": "xxxxx-yyyyy"})
    assert 'Start' in rec
    assert 'End' in rec
    assert 'RequestId' in rec

def test_connection():
    # can we assume role?
    obj = cr.CostReporter()
    assert isinstance(obj.sts, botocore.client.BaseClient)
    assert str(obj.sts.__class__) == "<class 'botocore.client.STS'>"
