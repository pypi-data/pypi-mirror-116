'''
# jsii-code-samples [![NPM](https://img.shields.io/npm/v/jsii-code-samples)](https://www.npmjs.com/package/jsii-code-samples) [![PyPI](https://img.shields.io/pypi/v/aws-jsiisamples.jsii-code-samples)](https://pypi.org/project/aws-jsiisamples.jsii-code-samples/) [![Maven](https://img.shields.io/maven-central/v/software.aws.jsiisamples.jsii/jsii-code-samples)](https://search.maven.org/artifact/software.aws.jsiisamples.jsii/jsii-code-samples) [![NuGet](https://img.shields.io/nuget/v/AWSSamples.Jsii)](https://www.nuget.org/packages/AWSSamples.Jsii/)

> An example jsii package authored in TypeScript that gets published as GitHub packages for Node.js, Python, Java and dotnet.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *


class CommonCheckWidget(
    metaclass=jsii.JSIIMeta,
    jsii_type="common-check-widget-backend-lib.CommonCheckWidget",
):
    def __init__(self) -> None:
        jsii.create(CommonCheckWidget, self, [])

    @jsii.member(jsii_name="ccw")
    def ccw(self, encryption_file: typing.Any, callback: typing.Any) -> None:
        '''
        :param encryption_file: -
        :param callback: -
        '''
        return typing.cast(None, jsii.invoke(self, "ccw", [encryption_file, callback]))

    @jsii.member(jsii_name="ccwasync")
    def ccwasync(self, encryption_file: typing.Any) -> typing.Any:
        '''
        :param encryption_file: -
        '''
        return typing.cast(typing.Any, jsii.ainvoke(self, "ccwasync", [encryption_file]))

    @jsii.member(jsii_name="cwsignin")
    def cwsignin(self, callback: typing.Any) -> None:
        '''
        :param callback: -
        '''
        return typing.cast(None, jsii.invoke(self, "cwsignin", [callback]))

    @jsii.member(jsii_name="cwsigninasync")
    def cwsigninasync(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.ainvoke(self, "cwsigninasync", []))


__all__ = [
    "CommonCheckWidget",
]

publication.publish()
