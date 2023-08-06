import time

import pytest

from aiojaeger.helpers import filter_none, make_timestamp
from aiojaeger.spancontext.zipkin import ZipkinConst, ZipkinTraceContext


@pytest.fixture
def trace_context():
    new_context = ZipkinTraceContext(
        trace_id=int("6f9a20b5092fa5e144fd15cc31141cd4", 16),
        parent_id=0,
        span_id=int("41baf1be2fb9bfc5", 16),
        sampled=True,
        debug=False,
        shared=False,
    )
    return new_context


@pytest.fixture
def other_trace_context():
    context = ZipkinTraceContext(
        trace_id=int("6f9a20b5092fa5e144fd15cc31141cd4", 16),
        parent_id=int("05e3ac9a4f6e3b90", 16),
        span_id=int("41baf1be2fb9bfc5", 16),
        sampled=True,
        debug=True,
        shared=False,
    )
    return context


def test_make_headers(trace_context):
    headers = ZipkinTraceContext.make_headers(trace_context)
    expected = {
        "X-B3-Flags": "0",
        "X-B3-Sampled": "1",
        "X-B3-SpanId": "41baf1be2fb9bfc5",
        "X-B3-TraceId": "6f9a20b5092fa5e144fd15cc31141cd4",
    }
    headers2 = trace_context.make_headers()
    assert headers == expected == headers2


def test_make_single_header(trace_context, other_trace_context):
    headers = ZipkinConst.make_single_header(trace_context)
    expected = {"b3": "6f9a20b5092fa5e144fd15cc31141cd4-41baf1be2fb9bfc5-1"}
    headers2 = trace_context.make_single_header()
    assert headers == expected == headers2

    headers = ZipkinConst.make_single_header(other_trace_context)
    h = "6f9a20b5092fa5e144fd15cc31141cd4-41baf1be2fb9bfc5-d-05e3ac9a4f6e3b90"
    headers2 = other_trace_context.make_single_header()
    expected = {"b3": h}
    assert headers == expected == headers2

    new_context = trace_context.copy(update=dict(debug=True, sampled=None))
    headers = ZipkinConst.make_single_header(new_context)
    expected = {"b3": "6f9a20b5092fa5e144fd15cc31141cd4-41baf1be2fb9bfc5-d"}
    assert headers == expected

    new_context = trace_context.copy(update=dict(debug=False, sampled=None))
    headers = ZipkinConst.make_single_header(new_context)
    expected = {"b3": "6f9a20b5092fa5e144fd15cc31141cd4-41baf1be2fb9bfc5-0"}
    assert headers == expected


def test_make_context(trace_context):
    headers = ZipkinConst.make_headers(trace_context)
    context = ZipkinConst.make_context(headers)
    assert trace_context == context

    context = ZipkinTraceContext.make_context({})
    assert context is None


def test_make_context_single_header(trace_context, other_trace_context):
    headers = ZipkinConst.make_single_header(trace_context)
    context = ZipkinTraceContext.make_context(headers)
    assert trace_context == context

    headers = ZipkinConst.make_single_header(other_trace_context)
    context = ZipkinTraceContext.make_context(headers)
    assert other_trace_context == context

    headers = {"b3": "0"}
    context = ZipkinTraceContext.make_context(headers)
    assert context is None

    headers = {"b3": "6f9a20b5092fa5e144fd15cc31141cd4"}
    context = ZipkinTraceContext.make_context(headers)
    assert context is None


def test_make_timestamp():
    ts = make_timestamp()
    assert len(str(ts)) == 16

    ts = make_timestamp(time.time())
    assert len(str(ts)) == 16


def test_filter_none():
    r = filter_none({"a": 1, "b": None})
    assert r == {"a": 1}

    r = filter_none({"a": 1, "b": None, "c": None}, keys=["a", "c"])
    assert r == {"a": 1, "b": None}

    r = filter_none({}, keys=["a", "c"])
    assert r == {}

    r = filter_none({"a": 1, "b": None, "c": {"c": None}}, keys=["a", "c"])
    assert r == {"a": 1, "b": None, "c": {"c": None}}
