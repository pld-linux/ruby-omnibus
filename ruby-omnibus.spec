#
# Conditional build:
%bcond_with	tests		# build without tests

%define	pkgname	omnibus
Summary:	Omnibus helps you build self-installing, full-stack software builds
Name:		ruby-%{pkgname}
Version:	1.0.4
Release:	1
License:	Apache v2.0
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	4ae9235161a1553a87abca21f6672414
URL:		https://github.com/opscode/omnibus-ruby
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	ruby-rspec
BuildRequires:	ruby-rspec_junit_formatter
%endif
Requires:	ruby-fpm < 0.5
Requires:	ruby-fpm >= 0.4.33
Requires:	ruby-mixlib-config < 1.2
Requires:	ruby-mixlib-config >= 1.1.2
Requires:	ruby-mixlib-shellout < 2
Requires:	ruby-mixlib-shellout >= 1.0
Requires:	ruby-ohai >= 0.6.12
Requires:	ruby-rake >= 0.9
Requires:	ruby-thor >= 0.16.0
Requires:	ruby-uber-s3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Omnibus helps you build self-installing, full-stack software builds.

%prep
%setup -q -n %{pkgname}-%{version}
%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{_bindir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/omnibus
%{ruby_vendorlibdir}/%{pkgname}.rb
%{ruby_vendorlibdir}/%{pkgname}
